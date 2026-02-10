{pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
	name = "news-api";
	
	packages = [
		pkgs.python312
		pkgs.uv
	];
	
	
  shellHook = ''
    echo "🚀 Entered news-api dev shell"

    if [ ! -d .venv ]; then
      echo "📦 Creating virtual environment"
      uv venv
    fi

    source .venv/bin/activate
  '';

}
