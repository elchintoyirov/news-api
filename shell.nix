{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "news-api";

  packages = [
    pkgs.python312
    pkgs.uv
    pkgs.gcc
    pkgs.gnumake
    pkgs.libffi
    pkgs.openssl
    pkgs.zlib
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${pkgs.gcc.cc.lib}/lib"
    echo "Entered news-api dev shell"

    if [ ! -d .venv ]; then
      echo "📦 Creating virtual environment"
      uv venv
    fi

    source .venv/bin/activate
    uv sync
  '';
}
