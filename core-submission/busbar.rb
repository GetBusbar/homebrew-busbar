class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  url "https://github.com/GetBusbar/busbar/archive/refs/tags/v1.4.0.tar.gz"
  sha256 "f95feeb0a41711d0f55cf97e75c2707d41f25ab2ea32b2c9d982cabe7aaf6304"
  license "Apache-2.0"
  head "https://github.com/GetBusbar/busbar.git", branch: "main"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args(path: "crates/busbar")
    # Ship the default provider catalog the gateway looks for at runtime.
    (etc/"busbar").install "providers.yaml"
  end

  def caveats
    <<~EOS
      To use the bundled provider catalog, set:
        export BUSBAR_PROVIDERS="#{etc}/busbar/providers.yaml"
      The gateway otherwise looks in /etc/busbar, outside the Homebrew prefix.
      Supply your gateway configuration separately via BUSBAR_CONFIG.
    EOS
  end

  test do
    expected = version.head? ? "busbar " : "busbar #{version}"
    assert_match expected, shell_output("#{bin}/busbar --version")
  end
end
