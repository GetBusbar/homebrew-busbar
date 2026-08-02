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
      sha256 "2b0e980555216f0a65d6ec50a947b2b24f6d95b4e58f4bd8db6f0eabe84a7769"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "c54a8b5f742ed3092126042fc5e10256477ce6eca005013335ced768e29dba0d"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "9bc246991e604fbf635ab34b95c3ad6afe323fb00fe4562d1dbc8f82117d5498"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "c07c7a7cc315342b568876ca8152f4491bda6df12c096828ccd7797c71715a8e"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
