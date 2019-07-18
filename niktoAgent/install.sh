#!/bin/bash

apt-get update
apt-get install python3 xinetd -y
python3 deploy.py