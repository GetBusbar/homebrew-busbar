# busbar-admin — the human-facing CLI for the Busbar gateway's admin API.
# Installs the prebuilt, release binary from GitHub Releases; the
# .github/workflows/bump.yml workflow keeps the version + checksums current.
class BusbarAdmin < Formula
  desc "CLI for the Busbar gateway admin API (info, keys, hooks, config)"
  homepage "https://getbusbar.com/docs/sdks/#busbar-admin-cli"
  version "0.2.1"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar-admin/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-admin-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "e7508d1ac119579cb9534ceb8a89f95c0f2d4d1119d8eef26518e1a31309bac7"
    end
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "6b36361923b4b3faf58e15d5f316a29f28b78a81e55fc5dd5b2df424822287f0"
    end
  end

  on_linux do
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "efa54b847341a9976e8abef8c702752ec4b95daaa441c10a9478335986fa8998"
    end
  end

  def install
    bin.install "busbar-admin"
  end

  test do
    assert_match "busbar-admin #{version}", shell_output("#{bin}/busbar-admin --version")
  end
end
