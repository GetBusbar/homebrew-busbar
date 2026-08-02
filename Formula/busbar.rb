# Busbar — single static-binary LLM gateway (your AI control plane).
# This formula installs the prebuilt, release-signed binary from GitHub Releases;
# the .github/workflows/bump.yml workflow keeps the version + checksums current.
class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  version "1.5.0"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-aarch64-apple-darwin.tar.gz"
      sha256 "d6e5ecbbe64e2e96c4be6be12dfd003a0f96dfc6ca185e4161eb3e4027daef60"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "74555d62ef67e7d0f5662259943a63caeb21e32cd9ccd0d47d67243f2073f568"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "073c2e5481a36237dfb612804432b72cfbf1b23f60ef5877b6794f31ad58ca11"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "08bc4407b95ae4dc71bb2c9108fa3d66444805be9cf81ef4f16de0df5669d744"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
