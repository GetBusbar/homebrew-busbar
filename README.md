# homebrew-busbar

Homebrew tap for [Busbar](https://getbusbar.com) — a single static-binary LLM gateway.

```sh
brew tap GetBusbar/busbar
brew trust GetBusbar/busbar   # Homebrew 6+ requires trusting a third-party tap once
brew install busbar

busbar --version
```

> On Homebrew 6 and newer, a third-party tap must be trusted once before its formulae will load (`brew trust GetBusbar/busbar`). Older Homebrew versions skip this step.

The formula installs the prebuilt, release-signed binary from [GitHub Releases](https://github.com/GetBusbar/busbar/releases) (macOS and Linux, Apple Silicon + Intel). To verify provenance independently:

```sh
gh attestation verify "$(brew --prefix)/bin/busbar" --repo GetBusbar/busbar
```

## Upgrading

```sh
brew update && brew upgrade busbar
```

The formula is kept current automatically: a scheduled workflow in this tap watches the upstream releases and bumps the version + checksums when a new one ships (see `.github/workflows/bump.yml`).
