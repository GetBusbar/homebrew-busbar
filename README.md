# homebrew-busbar

Homebrew tap for [Busbar](https://getbusbar.com) — a single static-binary LLM gateway.

```sh
brew tap GetBusbar/busbar
brew install busbar

busbar --version
```

The formula installs the prebuilt, release-signed binary from [GitHub Releases](https://github.com/MattJackson/busbarAI/releases) (macOS and Linux, Apple Silicon + Intel). To verify provenance independently:

```sh
gh attestation verify "$(brew --prefix)/bin/busbar" --repo MattJackson/busbarAI
```

## Upgrading

```sh
brew update && brew upgrade busbar
```

The formula is kept current automatically: a scheduled workflow in this tap watches the upstream releases and bumps the version + checksums when a new one ships (see `.github/workflows/bump.yml`).
