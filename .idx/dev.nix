{ pkgs, ... }:

{
  channel = "stable-23.11";

  packages = [
    pkgs.python311
    pkgs.nodejs_20
    pkgs.nodePackages.npm
    pkgs.sqlite
    pkgs.stdenv.cc.cc.lib
  ];

  env = {
    PYTHONUNBUFFERED = "1";
  };
}