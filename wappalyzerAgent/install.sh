#!/bin/bash
apt-get update
apt-get install curl -y
curl -sL https://deb.nodesource.com/setup_11.x | bash -
apt-get install python3 xinetd nodejs -y
npm i -g wappalyzer
python3 deploy.py