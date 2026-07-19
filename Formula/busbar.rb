# Busbar — single static-binary LLM gateway (your AI control plane).
# This formula installs the prebuilt, release-signed binary from GitHub Releases;
# the .github/workflows/bump.yml workflow keeps the version + checksums current.
class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  version "1.4.0"
  license "Apache-2.0"

  BASE = "https://github.com/MattJackson/busbarAI/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-aarch64-apple-darwin.tar.gz"
      sha256 "f20438796e8b411b915d7589338a44d3a87968749cef07a70b591f31cd2ecc3a"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "8dcf05757830c518b78d9d155f51db9d574cd4a41033ea26fad221f912a077fe"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "3d8ff47aa5aa6979d7d4798762b7b728674b3455157afe11725357c14949280d"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "98c286e76791be3046cc194ca5a268ae35b1228e951ac50b059ee959a18a096e"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
