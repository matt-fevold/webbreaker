class Webbreaker < Formula
  include Language::Python::Virtualenv

  desc "Webbreaker: Dynamic Application Security Test Orchestration"
  homepage "https://github.com/target/webbreaker"
  url "https://github.com/target/webbreaker/archive/latest.tar.gz"
  version "2.1.1"
  sha256 "465fa64e34db705668d5371fc8c565af232c32718bbd09e3627f2d9504862f31"

  def install
    venv = virtualenv_create(libexec)
    system libexec/"bin/pip", "install", "pyOpenSSL"
    system libexec/"bin/pip", "install", "wheel"
    system libexec/"bin/pip", "install", "pyinstaller==3.3"
    system libexec/"bin/pip", "install", "-r", "requirements.txt"

    system libexec/"bin/pyinstaller", "--clean", "-y", "--nowindowed", "--console", "--onefile",
                                      "--name", "webbreaker", "--osx-bundle-identifier",
                                      "com.target.ps.webbreaker", "-p",
                                      libexec/"bin/python", "webbreaker/__main__.py"
    bin.install Dir["dist/*"]
  end

  test do
    ENV["LC_ALL"] = "en_US.UTF-8"
    system "#{bin}/webbreaker", "--help"
  end
end
