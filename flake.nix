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
          pkgs.foreman
        ];
        shellHook = ''
          export PATH=$PWD/node_modules/.bin:$PATH
          alias dump_db="sqlite3 local.db 'SELECT * FROM name'"
          echo "Run 'foreman start' to run backend and frontend services"
          echo "service PORTs will be on 5000 and 100 increments beyond that"
        '';
      };
  };
}
