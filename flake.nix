{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixpkgs-python = {
      url = "github:cachix/nixpkgs-python";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs @ {
    self,
    nixpkgs,
    devenv,
    ...
  }: let
    system = "x86_64-linux";
    #    pkgs = nixpkgs.legacyPackages.${system};
    pkgs = import nixpkgs {
      inherit system;
      config = {
        allowUnfree = true;
        #        cudaSupport = true;
      };
    };
  in {
    devShells.${system}.default = devenv.lib.mkShell {
      inherit inputs pkgs;
      modules = [
        ({
          pkgs,
          config,
          ...
        }: {
          # This is your devenv configuration
          # for options see https://devenv.sh/reference/options/
          packages = with pkgs; [
            cudaPackages.cudatoolkit
            # from https://github.com/cachix/devenv/issues/1264#issuecomment-2368362686
            stdenv.cc.cc.lib # required by jupyter
            gcc-unwrapped # fix: libstdc++.so.6: cannot open shared object file
            libz # fix: for numpy/pandas import
          ];

          languages.python = {
            enable = true;
            version = "3.11";
            venv = {
              enable = true;
              requirements = ./requirements.txt;
            };
          };
          languages.rust.enable = true;

          # for cuda support
          # https://discourse.nixos.org/t/pytorch-installed-via-pip-does-not-pick-up-cuda/30744/2
          # https://github.com/clementpoiret/nix-python-devenv/blob/main/flake.nix
          env.LD_LIBRARY_PATH = "${pkgs.gcc-unwrapped.lib}/lib64:${pkgs.libz}/lib:/run/opengl-driver/lib:/run/opengl-driver-32/lib";
          env.PYTHONPATH = "/home/wolfingten/projects/self-attentive-parser/src/";

          enterShell = ''
          '';
        })
      ];
    };
  };
}
