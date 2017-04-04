#!/usr/bin/env bash

apt-get update && apt-get upgrade -y
apt-get install git python3 python3-pip -y

git clone https://github.com/gitcommitpush/composer.git
cd composer

pip3 install -r requirements.txt

mkdir data
mkdir data/apps
mkdir data/log
