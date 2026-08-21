# busbar-admin — the human-facing CLI for the Busbar gateway's admin API.
# Installs the prebuilt, release binary from GitHub Releases; the
# .github/workflows/bump.yml workflow keeps the version + checksums current.
class BusbarAdmin < Formula
  desc "CLI for the Busbar gateway admin API (info, keys, hooks, config)"
  homepage "https://getbusbar.com/docs/sdks/#busbar-admin-cli"
  version "0.2.4"
  license "Apache-2.0"

  BASE = "https://github.com/GetBusbar/busbar-admin/releases/download/v#{version}".freeze

  on_macos do
    on_arm do
      url "#{BASE}/busbar-admin-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "f317563423b02131ddeeccd3cfec5ad6b9d980ae87851dc1d42ffe034da816a5"
    end
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "d2809dbfd87324913c42956232fa664c3a87d3bb527afba7e837c2645ede2015"
    end
  end

  on_linux do
    on_intel do
      url "#{BASE}/busbar-admin-v#{version}-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "75d56273c004b052f68f8e21b52fa265a859316acc56d2a2b486c355df7e0941"
    end
  end

  def install
    bin.install "busbar-admin"
  end

  test do
    assert_match "busbar-admin #{version}", shell_output("#{bin}/busbar-admin --version")
  end
end
