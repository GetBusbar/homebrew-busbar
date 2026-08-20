# Busbar — single static-binary LLM gateway (your AI control plane).
# This formula installs the prebuilt, release-signed binary from GitHub Releases;
# the .github/workflows/bump.yml workflow keeps the version + checksums current.
class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  version "1.5.5"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-aarch64-apple-darwin.tar.gz"
      sha256 "93f8f02a018c0f476c36a84aceb3e851999bee09584114ba01e2a9bd309e3c1b"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "56438c6fcd3ece46bdaa17b49cdcf965697205331842eaeb0dec1d6a36fab9f9"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "6f8ab606b81ea8326813a991729fefe237d607c89bbcc433c1d5000a8257c8ac"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "64f0eda182c803ebff691d91e71a2dae468d759d73d646b13a0b1b1df06ddd9d"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
