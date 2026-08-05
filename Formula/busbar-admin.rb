# busbar-admin — the human-facing CLI for the Busbar gateway's admin API.
# Installs the prebuilt, release binary from GitHub Releases; the
# .github/workflows/bump.yml workflow keeps the version + checksums current.
class BusbarAdmin < Formula
  desc "CLI for the Busbar gateway admin API (info, keys, hooks, config)"
  homepage "https://getbusbar.com/docs/sdks/#busbar-admin-cli"
  version "0.2.2"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar-admin/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-admin-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "2f954c10952405adedd389fa45938444105947d9e95c75bd09cad8fca9ec2daa"
    end
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "59b6acee7aad479751c0dfc3801e7585106b3e95236ae6ad70b09e5a17b146e7"
    end
  end

  on_linux do
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "2cd3fdea6e55bd7c9df56f35dddff1422cebe6adbc2d24dcb650c52466cc8aeb"
    end
  end

  def install
    bin.install "busbar-admin"
  end

  test do
    assert_match "busbar-admin #{version}", shell_output("#{bin}/busbar-admin --version")
  end
end
