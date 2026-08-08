# busbar-admin — the human-facing CLI for the Busbar gateway's admin API.
# Installs the prebuilt, release binary from GitHub Releases; the
# .github/workflows/bump.yml workflow keeps the version + checksums current.
class BusbarAdmin < Formula
  desc "CLI for the Busbar gateway admin API (info, keys, hooks, config)"
  homepage "https://getbusbar.com/docs/sdks/#busbar-admin-cli"
  version "0.2.3"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar-admin/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-admin-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "d7457b2898ab288e88c7982e65864ed7a4b7a062f7c6af14c2659df392c3148f"
    end
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "acee9faa7d7c414fb9acc8e35c229db9b36429b6fbe6165c29ed8debe45c1516"
    end
  end

  on_linux do
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "a9da607a21b291549bdbc19af5f445cf3937f2a5b9c70ccd81695dd8ca425957"
    end
  end

  def install
    bin.install "busbar-admin"
  end

  test do
    assert_match "busbar-admin #{version}", shell_output("#{bin}/busbar-admin --version")
  end
end
