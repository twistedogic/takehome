# Take home project

## Project structure

* `infra`: terraform code for network and infrastructure setup
* `takemehome`: python module for API and client
* `scripts`: bash and python scripts for bootstrap server

## Infrastructure

### Prerequisites

* Install `terraform` following [here](https://developer.hashicorp.com/terraform/downloads)
* In order to provision AWS assets, `AWS` account with correct permission needs to
be configured. Access key and token should set as environment variables as below:

````
export AWS_ACCESS_KEY_ID=(your access key id)
export AWS_SECRET_ACCESS_KEY=(your secret access key)
export TF_VAR_pub_key_file=(file path to the ssh pub key for EC2 instance access)
````
### Initialize Infrastructure

```
cd infra
terraform Init 
terraform apply
```

### See current infrastructure diff

```
cd infra
terraform plan
```
## API

### Development

The following will start a local development API server listening on 0.0.0.0:3000 with live reload.

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirement.txt
pip install .
python3 -m takemehome
```

Go to `http://localhost:3000/` to access the swagger UI.

### Testing

`python3 -m unittest tests/test_api.py`

### Client

You can access the API via swagger UI under `/` or you can access via CLI client

#### Show all entries
`python3 -m takemehome.client --base_url http://<API host>:<API port> show`

#### Create entry
`python3 -m takemehome.client --base_url http://<API host>:<API port> create --username <username> --message <message>`

#### Update entry
`python3 -m takemehome.client --base_url http://<API host>:<API port> update --id <entry id to update> --username <username> --message <message>`

## Deployment

```
cd ~
git clone https://github.com/twistedogic/takehome.github
cd takehome
sudo sh scripts/setup.sh <sub-interface name> <IP address> <Net mask>
```

Example:
`sudo sh scripts/setup.sh eth0:1 10.0.2.100 255.255.255.0`

This example will setup the following:
* Setup sub-interface `eth0:1` with `10.0.2.100/24`.
    * File created under `/etc/sysconfig/network-scripts`
* Configure mysqld to listen only on `10.0.2.100`.
    * Config file updated in `/etc/my.cnf.d/mysql-server.cnf`
* Setup database user for connecting via `10.0.2.100` and permission for `tower` database.
* Setup systemd service unit in `/etc/systemd/system/takemehome.service` for API service.

