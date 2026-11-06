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
ANY_SHA_LINE = re.compile(r'^\s*sha256\b', re.MULTILINE)


def version_tuple(value):
    if not VERSION.fullmatch(value):
        raise ValueError("expected a stable release version MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in value.split("."))


def is_newer(source, version):
    matches = list(VERSION_LINE.finditer(source))
    if len(matches) != 1:
        raise ValueError("expected exactly one explicit formula version")
    current = matches[0].group(0).strip().split('"')[1]
    try:
        current_tuple = version_tuple(current)
    except ValueError:
        raise ValueError(f"formula version {current!r} is not MAJOR.MINOR.PATCH") from None
    return version_tuple(version) > current_tuple


def update(path, shas, version=None):
    if not shas or any(not re.fullmatch(r"[0-9a-f]{64}", sha) for sha in shas):
        raise ValueError("checksums must be 64 lowercase hexadecimal digits")
    if len(set(shas)) != len(shas):
        raise ValueError("duplicate checksums: each platform archive has its own sha256")
    source = path.read_text()
    current = [m[0].split('"')[1] for m in SHA_LINE.finditer(source)]
    if len(current) != len(ANY_SHA_LINE.findall(source)):
        raise ValueError("formula has a malformed sha256 line (expected 64 lowercase hex digits)")
    if len(current) != len(shas):
        raise ValueError("checksum count does not match formula")
    if version is not None:
        if not is_newer(source, version):
            raise ValueError("release version must be newer than the formula")
        if set(shas) & set(current):
            raise ValueError("a new release cannot reuse the previous release's checksums")
        source = VERSION_LINE.sub(lambda m: f"{m[1]}{version}{m[2]}", source)
    values = iter(shas)
    source = SHA_LINE.sub(lambda m: f"{m[1]}{next(values)}{m[2]}", source)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, prefix=f".{path.name}.",
                                         suffix=".tmp", delete=False) as out:
            temporary = Path(out.name)
            out.write(source)
            out.flush()
            os.fsync(out.fileno())
        temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
        # Best effort: the formula is already updated, so a failed directory sync must not
        # report the update as failed.
        try:
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        except OSError:
            pass
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", type=Path)
    parser.add_argument("shas", nargs="*")
    parser.add_argument("--version")
    parser.add_argument("--check-version")
    args = parser.parse_intermixed_args()  # checksums may follow --version on any Python 3
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
