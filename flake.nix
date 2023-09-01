{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  outputs = {
    self,
    nixpkgs,
  }: {
    devShells.x86_64-linux.default = let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
      pkgs.mkShell {
        name = "new-website";
        packages = [
          pkgs.nodejs
          pkgs.poetry
          pkgs.sqlite
        ];
        shellHook = ''
          export PATH=$PWD/node_modules/.bin:$PATH
        '';
      };
  };
}
