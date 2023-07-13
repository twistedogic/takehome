#!/bin/bash

echo "setup mysql, python and git"
sudo dnf install -y mysql-server python3 git
sudo systemctl start mysqld.service
sudo systemctl enable mysqld.service

