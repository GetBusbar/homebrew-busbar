# Busbar — single static-binary LLM gateway (your AI control plane).
# This formula installs the prebuilt, release-signed binary from GitHub Releases;
# the .github/workflows/bump.yml workflow keeps the version + checksums current.
class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  version "1.4.1"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-aarch64-apple-darwin.tar.gz"
      sha256 "e62631f2463b81052ca66c57004f4f5385395313de735ce6109351ba75c461a7"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "89de2e05a709125b8daaa1b3a5bd7b70385104870e02fc59c9c6f8797dbb3f96"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "f5709611d6c6aa5f07855b67ccc16a6692e6e7cbc3d3376ebde12c1426a50e79"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "4aa9228e45e2b9511f77b5458c314de4ec7009068590e7576dbcf96d933ab582"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
