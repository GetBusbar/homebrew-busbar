# Busbar — single static-binary LLM gateway (your AI control plane).
# This formula installs the prebuilt, release-signed binary from GitHub Releases;
# the .github/workflows/bump.yml workflow keeps the version + checksums current.
class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  version "1.5.2"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-aarch64-apple-darwin.tar.gz"
      sha256 "4885fc1164f389a099857d77da2f20989b2866a40e94145a90a4716605e1a506"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-apple-darwin.tar.gz"
      sha256 "1cf0e6ef5afd9285a58ebd3e8d36e48f01242b8173666b252a73ef5da0883264"
    end
  end

  on_linux do
    on_arm do
      url "#{BASE}/busbar-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "f249fef7f853630b52a9bdbee825ad1f84312e2e95025a95b33e9ecfb0b9e2e0"
    end
    on_intel do
      url "#{BASE}/busbar-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "e4434c5693387d4b10a06941b16eb419f9050a4e69f9e6ea2a857e284f79f426"
    end
  end

  def install
    bin.install "busbar"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
