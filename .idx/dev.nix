{ pkgs, ... }:

{
  channel = "stable-23.11";

  packages = [
    pkgs.python311
    pkgs.python311Packages.requests
    pkgs.nodejs_20
    pkgs.sqlite
    pkgs.stdenv.cc.cc.lib
    pkgs.openssh
  ];

  env = {
    PYTHONUNBUFFERED = "1";
  };
}