{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.requests
    python3Packages.beautifulsoup4
  ];
  
  shellHook = ''
    echo "🐍 Python environment ready!"
    echo "Python: $(python3 --version)"
    echo "Run: python3 download_icons.py"
  '';
}

