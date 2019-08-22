#!/bin/bash

apt-get update
apt-get install python3 python3-pip xinetd -y
pip3 install requests
python3 deploy.py