# homebrew-core submission (source build)

This directory holds a **core-ready, build-from-source** formula for `busbar`, kept
separate from the tap's `Formula/busbar.rb` (which installs the prebuilt release
binary for fast local installs).

`homebrew-core` does **not** accept prebuilt-binary formulae — it compiles from
source. This `busbar.rb` does that (`depends_on "rust" => :build`, `cargo install`),
and has been verified locally:

- builds from the `v1.4.0` source tarball (full Rust tree incl. jemalloc) — ~90s
- `brew test` passes (`busbar --version`)
- `brew audit --new --strict` → exit 0
- `brew style` → no offenses

## To submit to homebrew-core

1. Bump `url`/`sha256` to the version you want to ship.
2. `brew tap homebrew/core --force` (get a local core checkout), copy this file to
   `$(brew --repository homebrew/core)/Formula/b/busbar.rb`.
3. `brew audit --new --strict busbar` and `brew install --build-from-source busbar`
   one more time, then open a PR to homebrew/homebrew-core.

Remaining gates are outside the formula: (a) Homebrew's Linux CI must build it
(jemalloc-on-Linux), and (b) **notability** — core reviewers gauge project traction,
and are wary of brand-new self-submissions. Best submitted once the project has
more stars/usage.
