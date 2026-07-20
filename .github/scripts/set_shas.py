#!/usr/bin/env python3
"""set_shas.py <formula.rb> <sha1> <sha2> ...  — replace the sha256 "..." lines in file order."""
import re, sys
p, shas = sys.argv[1], sys.argv[2:]
s = open(p).read(); i = 0
def repl(m):
    global i
    if i >= len(shas): sys.exit(f"more sha256 lines than provided shas ({len(shas)})")
    out = f'{m.group(1)}{shas[i]}{m.group(2)}'; i += 1; return out
s = re.sub(r'(sha256 ")[0-9a-f]{64}(")', repl, s)
if i != len(shas): sys.exit(f"expected {len(shas)} sha256 lines, replaced {i}")
open(p, "w").write(s); print(f"set {i} sha256(s) in {p}")
