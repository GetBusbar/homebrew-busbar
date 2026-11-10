# homebrew-busbar

Homebrew tap for [Busbar](https://getbusbar.com) — a single-binary LLM gateway.

```sh
brew tap GetBusbar/busbar
brew trust GetBusbar/busbar   # Homebrew 6+ requires trusting a third-party tap once
brew install busbar

busbar --version
```

> On Homebrew 6 and newer, a third-party tap must be trusted once before its formulae will load (`brew trust GetBusbar/busbar`). Older Homebrew versions skip this step.

The formula installs the prebuilt binary from [GitHub Releases](https://github.com/GetBusbar/busbar/releases) (macOS and Linux, Apple Silicon + Intel). To verify provenance independently:

```sh
brew fetch GetBusbar/busbar/busbar
gh attestation verify "$(brew --cache GetBusbar/busbar/busbar)" --repo GetBusbar/busbar
```

Attestations cover the downloaded release archive, not the extracted executable.
The commands above verify the version currently selected by the tap.

## busbar-admin

The tap also ships `busbar-admin`, the CLI for the gateway's admin API:

```sh
brew install busbar-admin
```

Prebuilt for macOS (Apple Silicon + Intel) and Linux x86_64; there is no Linux arm64 build.

## Upgrading

```sh
brew update && brew upgrade busbar
brew upgrade busbar-admin   # if installed
```

Formula updates are maintained on the private Gitea repository and mirrored here.
Version and checksum updates must refer to the approved release artifacts.
