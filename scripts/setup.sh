#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

APP_HOME=$SCRIPT_DIR/..

cd $APP_HOME

python3 -m venv venv
. venv/bin/activate

pip install -r requirement.txt
pip install .

# set selinux context for executing binary from virtualenv
sudo chcon -Rv -u system_u -t bin_t venv/{bin,lib}

sudo python3 scripts/bootstrap.py $1 $2 $3 --venv $APP_HOME/venv --dir $APP_HOME
