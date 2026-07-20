class Busbar < Formula
  desc "Single-binary LLM gateway — one API in front of every model and provider"
  homepage "https://getbusbar.com"
  url "https://github.com/MattJackson/busbarAI/archive/refs/tags/v1.4.0.tar.gz"
  sha256 "3770eb4a51eb3fbb30c14551fbab1c6c046902eba57ba5df64eda0b9d84347f6"
  license "Apache-2.0"
  head "https://github.com/MattJackson/busbarAI.git", branch: "main"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args(path: "crates/busbar")
    # Ship the default provider catalog the gateway looks for at runtime.
    (etc/"busbar").install "providers.yaml"
  end

  test do
    assert_match "busbar #{version}", shell_output("#{bin}/busbar --version")
  end
end
