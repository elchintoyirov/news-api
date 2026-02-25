{
  devShells.default = pkgs.mkShell {
    buildInputs = [ pkgs.python312 ];
  };
}
