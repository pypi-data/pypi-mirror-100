#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : apksigcopier
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2021-03-26
#
# Copyright   : Copyright (C) 2021  Felix C. Stegerman
# Version     : v0.1.0
# License     : GPLv3+
#
# --                                                            ; }}}1

"""
copy/extract/patch apk signatures
"""

import glob
import os
import shutil
import subprocess
import tempfile
import zipfile
import zlib

from collections import namedtuple

__version__ = "0.1.0"
name = "apksigcopier"

SIGBLOCK, SIGOFFSET = "APKSigningBlock", "APKSigningBlockOffset"
APKSIGNER_CMD, KEYTOOL_CMD, ZIP_CMD = "apksigner keytool zip".split()
NOAUTOYES = NO, AUTO, YES = "no auto yes".split()

ZipData = namedtuple("ZipData", "cd_offset eocd_offset cd_and_eocd".split())


# FIXME
class ReproducibleZipInfo(zipfile.ZipInfo):
    """Reproducible ZipInfo hack."""

    _override = {}

    def __init__(self, zinfo):
        for k in self.__slots__:
            if hasattr(zinfo, k):
                setattr(self, k, getattr(zinfo, k))

    def __getattribute__(self, name):
        try:
            return type(self)._override[name]
        except KeyError:
            return object.__getattribute__(self, name)


class APKZipInfo(ReproducibleZipInfo):
    """Reproducible ZipInfo for APK files."""

    _override = dict(
        compress_type=8,
        create_system=0,
        create_version=20,
        date_time=(1980, 0, 0, 0, 0, 0),
        external_attr=0,
        extract_version=20,
        flag_bits=0x800,
    )


# FIXME: .DSA?
def is_meta(filename):
    return filename.startswith("META-INF") and \
        any(filename.endswith(ext) for ext in ".SF .RSA .MF".split())


def noautoyes(value):
    if isinstance(value, str):
        assert value in NOAUTOYES
        return value
    return {False: NO, None: AUTO, True: YES}[value]


def remove_from_zip(zipfile, files, zip_cmd=ZIP_CMD):
    subprocess.run([zip_cmd, "-q", "-d", zipfile] + list(files), check=True)


def gen_dummy_key(keystore, alias="dummy", keyalg="RSA", keysize=4096,
                  sigalg="SHA512withRSA", validity=10000,
                  storepass="dummy-password", dname="CN=dummy",
                  keytool_cmd=KEYTOOL_CMD):
    """Generate a dummy key using keytool."""
    args = [
        keytool_cmd, "-genkey", "-keystore", keystore, "-alias", alias,
        "-keyalg", keyalg, "-keysize", str(keysize), "-sigalg", sigalg,
        "-validity", str(validity), "-storepass", storepass, "-dname", dname
    ]
    subprocess.run(args, check=True)


def sign_with_dummy_key(output_apk, keystore, alias="dummy",
                        ks_pass="pass:dummy-password",
                        apksigner_cmd=APKSIGNER_CMD):
    """Sign APK with dummy key using apksigner."""
    args = [
        apksigner_cmd, "sign", "--ks", keystore, "--ks-key-alias", alias,
        "--ks-pass", ks_pass, output_apk
    ]
    subprocess.run(args, check=True)


def extract_meta(signed_apk):
    """Extract v1 signature metadata files from signed APK."""
    with zipfile.ZipFile(signed_apk, "r") as zf_sig:
        for info in zf_sig.infolist():
            if is_meta(info.filename):
                yield info, zf_sig.read(info.filename)


def replace_meta(extracted_meta, output_apk, zip_cmd=ZIP_CMD):
    """Replace v1 signature metadata in signed APK (removes v2 sig block)."""
    with zipfile.ZipFile(output_apk, "r") as zf_out:
        meta = [info.filename for info in zf_out.infolist()
                if is_meta(info.filename)]
        remove_from_zip(output_apk, meta, zip_cmd=zip_cmd)
    with zipfile.ZipFile(output_apk, "a") as zf_out:
        if "compresslevel" in zipfile.ZipFile.__doc__:         # FIXME
            for info, data in extracted_meta:
                zf_out.writestr(APKZipInfo(info), data, compresslevel=9)
        else:
            old = zipfile._get_compressor
            zipfile._get_compressor = lambda _: zlib.compressobj(9, 8, -15)
            try:
                for info, data in extracted_meta:
                    zf_out.writestr(APKZipInfo(info), data)
            finally:
                zipfile._get_compressor = old


# https://source.android.com/security/apksigning/v2#apk-signing-block-format
# https://en.wikipedia.org/wiki/ZIP_(file_format)#End_of_central_directory_record_(EOCD)
#
# =================================
# | Contents of ZIP entries       |
# =================================
# | APK Signing Block             |
# | ----------------------------- |
# | | size (w/o this) uint64 LE | |
# | | ...                       | |
# | | size (again)    uint64 LE | |
# | | "APK Sig Block 42" (16B)  | |
# | ----------------------------- |
# =================================
# | ZIP Central Directory         |
# =================================
# | ZIP End of Central Directory  |
# | ----------------------------- |
# | | 0x06054b50 ( 4B)          | |
# | | ...        (12B)          | |
# | | CD Offset  ( 4B)          | |
# | | ...                       | |
# | ----------------------------- |
# =================================


def extract_v2_sig(apkfile, expected=True, count=4096):
    """Extract APK Signing Block from APK."""
    with open(apkfile, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        data = b""
        sb_magic = -1
        while sb_magic < 0:
            if fh.tell() < count:
                if expected:
                    raise RuntimeError("No APK Sig Block")
                else:
                    return None
            fh.seek(-count, os.SEEK_CUR)
            data = (fh.read(count) + data)[:count * 2]
            fh.seek(-count, os.SEEK_CUR)
            sb_magic = data.rfind(b"APK Sig Block 4")
        fh.seek(sb_magic - 8, os.SEEK_CUR)
        sb_size2 = int.from_bytes(fh.read(8), "little")
        fh.seek(-sb_size2 + 8, os.SEEK_CUR)
        sb_size1 = int.from_bytes(fh.read(8), "little")
        assert sb_size1 == sb_size2
        fh.seek(-8, os.SEEK_CUR)
        sb_offset = fh.tell()
        sig_block = fh.read(sb_size2 + 8)
    return sb_offset, sig_block


def zip_data(apkfile, count=1024):
    """Extract central directory & EOCD from ZIP."""
    with open(apkfile, "rb") as fh:
        fh.seek(-count, os.SEEK_END)
        data = fh.read()
        fh.seek(data.rindex(b"\x50\x4b\x05\x06") - len(data), os.SEEK_CUR)
        eocd_offset = fh.tell()
        fh.seek(16, os.SEEK_CUR)
        cd_offset = int.from_bytes(fh.read(4), "little")
        fh.seek(cd_offset)
        cd_and_eocd = fh.read()
    return ZipData(cd_offset, eocd_offset, cd_and_eocd)


def patch_v2_sig(extracted_v2_sig, output_apk):
    """Implant extracted v2/v3 signature into APK."""
    signed_sb_offset, signed_sb = extracted_v2_sig
    data_out = zip_data(output_apk)
    padding = b"\x00" * (signed_sb_offset - data_out.cd_offset)
    offset = len(signed_sb) + len(padding)
    with open(output_apk, "r+b") as fh:
        fh.seek(data_out.cd_offset)
        fh.write(padding)
        fh.write(signed_sb)
        fh.write(data_out.cd_and_eocd)
        fh.seek(data_out.eocd_offset + offset + 16)
        fh.write(int.to_bytes(data_out.cd_offset + offset, 4, "little"))


def patch_apk(extracted_meta, extracted_v2_sig, unsigned_apk,
              output_apk, dummyks=None, config={}):
    """Patch extracted_meta + extracted_v2_sig onto unsigned_apk and save as output_apk."""
    apksigner_cmd = config.get("apksigner_cmd", APKSIGNER_CMD)
    keytool_cmd = config.get("keytool_cmd", KEYTOOL_CMD)
    zip_cmd = config.get("zip_cmd", ZIP_CMD)
    shutil.copy(unsigned_apk, output_apk)
    if dummyks is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dummyks = os.path.join(tmpdir, "dummy-keystore")
            gen_dummy_key(dummyks, keytool_cmd=keytool_cmd)
            sign_with_dummy_key(output_apk, dummyks, apksigner_cmd=apksigner_cmd)
    else:
        sign_with_dummy_key(output_apk, dummyks, apksigner_cmd=apksigner_cmd)
    replace_meta(extracted_meta, output_apk, zip_cmd=zip_cmd)
    if extracted_v2_sig is not None:
        patch_v2_sig(extracted_v2_sig, output_apk)


def do_extract(signed_apk, output_dir, v1_only=NO):
    """Extract signatures from signed_apk and save in output_dir."""
    v1_only = noautoyes(v1_only)
    extracted_meta = extract_meta(signed_apk)
    for info, data in extracted_meta:
        name = os.path.basename(info.filename)
        with open(os.path.join(output_dir, name), "wb") as fh:
            fh.write(data)
    if v1_only == YES:
        return
    expected = v1_only == NO
    extracted_v2_sig = extract_v2_sig(signed_apk, expected=expected)
    if extracted_v2_sig is None:
        return
    signed_sb_offset, signed_sb = extracted_v2_sig
    with open(os.path.join(output_dir, SIGOFFSET), "w") as fh:
        fh.write(str(signed_sb_offset) + "\n")
    with open(os.path.join(output_dir, SIGBLOCK), "wb") as fh:
        fh.write(signed_sb)


def do_patch(metadata_dir, unsigned_apk, output_apk, v1_only=NO,
             dummy_keystore=None, config={}):
    """Patch signatures from metadata_dir onto unsigned_apk and save as output_apk."""
    v1_only = noautoyes(v1_only)
    extracted_meta = []
    for what in "SF RSA MF".split():
        filename, = glob.glob(os.path.join(metadata_dir, "*." + what))
        info = zipfile.ZipInfo("META-INF/" + os.path.basename(filename))
        with open(filename, "rb") as fh:
            data = fh.read()
        extracted_meta.append((info, data))
    if v1_only == YES:
        extracted_v2_sig = None
    else:
        sigoffset_file = os.path.join(metadata_dir, SIGOFFSET)
        sigblock_file = os.path.join(metadata_dir, SIGBLOCK)
        if v1_only == AUTO and not os.path.exists(sigblock_file):
            extracted_v2_sig = None
        else:
            with open(sigoffset_file, "r") as fh:
                signed_sb_offset = int(fh.read())
            with open(sigblock_file, "rb") as fh:
                signed_sb = fh.read()
            extracted_v2_sig = signed_sb_offset, signed_sb
    patch_apk(extracted_meta, extracted_v2_sig, unsigned_apk, output_apk,
              dummy_keystore, config=config)


def do_copy(signed_apk, unsigned_apk, output_apk, v1_only=NO,
            dummy_keystore=None, config={}):
    """Copy signatures from signed_apk onto unsigned_apk and save as output_apk."""
    v1_only = noautoyes(v1_only)
    extracted_meta = extract_meta(signed_apk)
    if v1_only == YES:
        extracted_v2_sig = None
    else:
        expected = v1_only == NO
        extracted_v2_sig = extract_v2_sig(signed_apk, expected=expected)
    patch_apk(extracted_meta, extracted_v2_sig, unsigned_apk, output_apk,
              dummy_keystore, config=config)


def main():
    import click

    V1Only = click.Choice(NOAUTOYES)

    @click.group(help="""
        apksigcopier - copy/extract/patch apk signatures
    """)
    @click.version_option(__version__)
    @click.pass_context
    def cli(ctx):
        pass

    @cli.command(help="""
        Extract APK signatures from signed APK.
    """)
    @click.option("--v1-only", type=V1Only, default=NO, show_default=True)
    @click.argument("signed_apk", type=click.Path(exists=True, dir_okay=False))
    @click.argument("output_dir", type=click.Path(exists=True, file_okay=False))
    def extract(*args, **kwargs):
        do_extract(*args, **kwargs)

    @cli.command(help="""
        Patch extracted APK signatures onto unsigned APK.
    """)
    @click.option("--v1-only", type=V1Only, default=NO, show_default=True)
    @click.option("--dummy-keystore", type=click.Path(exists=True, dir_okay=False))
    @click.argument("metadata_dir", type=click.Path(exists=True, file_okay=False))
    @click.argument("unsigned_apk", type=click.Path(exists=True, dir_okay=False))
    @click.argument("output_apk", type=click.Path(dir_okay=False))
    def patch(*args, **kwargs):
        do_patch(*args, **kwargs)

    @cli.command(help="""
        Copy (extract & patch) signatures from signed to unsigned APK.
    """)
    @click.option("--v1-only", type=V1Only, default=NO, show_default=True)
    @click.option("--dummy-keystore", type=click.Path(exists=True, dir_okay=False))
    @click.argument("signed_apk", type=click.Path(exists=True, dir_okay=False))
    @click.argument("unsigned_apk", type=click.Path(exists=True, dir_okay=False))
    @click.argument("output_apk", type=click.Path(dir_okay=False))
    def copy(*args, **kwargs):
        do_copy(*args, **kwargs)

    @cli.command(help="""
        Generate dummy key(store).
    """)
    @click.option("--keysize", type=int, default=4096, show_default=True)
    @click.argument("dummy_keystore", type=click.Path(dir_okay=False))
    def gen_dummy(dummy_keystore, keysize):
        gen_dummy_key(dummy_keystore, keysize=keysize)

    cli(prog_name=name)


if __name__ == "__main__":
    main()

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
