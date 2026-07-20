# busbar-admin — the human-facing CLI for the Busbar gateway's admin API.
# Installs the prebuilt, release binary from GitHub Releases; the
# .github/workflows/bump.yml workflow keeps the version + checksums current.
class BusbarAdmin < Formula
  desc "CLI for the Busbar gateway admin API (info, keys, hooks, config)"
  homepage "https://getbusbar.com/docs/sdks/#busbar-admin-cli"
  version "0.1.0"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar-admin/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-admin-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "c50aa6b8cdf815a651c8a997ac3542d20001d4c9a4d4a48f9fe2ef4256465c53"
    end
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "b064636be75156f54aa5f22ac714327ffb036b5363f07edb3bf98d031fcc617b"
    end
  end

  on_linux do
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "d9a27857df72985d6710eb00575ef16180dbed08b11b446d492147d5b5ddcb18"
    end
  end

  def install
    bin.install "busbar-admin"
  end

  test do
    assert_match "busbar-admin #{version}", shell_output("#{bin}/busbar-admin --version")
  end
end
