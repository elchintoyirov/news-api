{
  description = "NewsAPI dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python312
            pkgs.gcc.cc.lib

            pkgs.gcc
            pkgs.gnumake
            pkgs.libffi
            pkgs.openssl
            pkgs.zlib
          ];
          
          shellHook = ''
            export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${pkgs.gcc.cc.lib}/lib"
          '';
        };
      });
}