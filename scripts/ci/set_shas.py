#!/usr/bin/env python3
"""Validate release versions and atomically update a formula's version/checksums."""

import argparse
import os
from pathlib import Path
import re
import tempfile

VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
VERSION_LINE = re.compile(r'^(\s*version ")[^"]+("[ \t]*)$', re.MULTILINE)
SHA_LINE = re.compile(r'^(\s*sha256 ")[0-9a-f]{64}("[ \t]*)$', re.MULTILINE)


def version_tuple(value):
    if not VERSION.fullmatch(value):
        raise ValueError("expected a stable release version MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in value.split("."))


def is_newer(source, version):
    matches = list(VERSION_LINE.finditer(source))
    if len(matches) != 1:
        raise ValueError("expected exactly one explicit formula version")
    current = matches[0].group(0).strip().split('"')[1]
    return version_tuple(version) > version_tuple(current)


def update(path, shas, version=None):
    if not shas or any(not re.fullmatch(r"[0-9a-f]{64}", sha) for sha in shas):
        raise ValueError("checksums must be 64 lowercase hexadecimal digits")
    source = path.read_text()
    if len(list(SHA_LINE.finditer(source))) != len(shas):
        raise ValueError("checksum count does not match formula")
    if version is not None:
        if not is_newer(source, version):
            raise ValueError("release version must be newer than the formula")
        source = VERSION_LINE.sub(lambda m: f"{m[1]}{version}{m[2]}", source)
    values = iter(shas)
    source = SHA_LINE.sub(lambda m: f"{m[1]}{next(values)}{m[2]}", source)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as out:
            temporary = Path(out.name)
            out.write(source)
        temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", type=Path)
    parser.add_argument("shas", nargs="*")
    parser.add_argument("--version")
    parser.add_argument("--check-version")
    args = parser.parse_args()
    try:
        if args.check_version is not None:
            if args.version is not None or args.shas:
                parser.error("--check-version cannot update the formula")
            print("newer" if is_newer(args.formula.read_text(), args.check_version) else "current")
        else:
            update(args.formula, args.shas, args.version)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
