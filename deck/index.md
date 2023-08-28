# SRE Take Home Project
## Agenda
- Requirements
- Demo
- Architecture
- Overview
- Development
- Deployment
- Out of scope items

---

# Requirements
- A one-time setup of the following:
    - Single EC2 instance of CentOS or Rocky linux 
    - A network sub-interface
    - MySQL server process to only listen on the network sub-interface
    - Database setup with table
- Python web service that can `create` or `update` database entries via network
- Source code should be in git

---

# Demo

![](http://bladerunnerjs.org/blog/img/demo-time.jpg)

___

# Architecture 

![bg center fit](diagrams/overview.svg)

---

# Overview

## Tech Stack

- `terraform` – AWS EC2 and network provision
- `Flask` – python web service framework
- `SQLAlchemy` – python SQL ORM
- `gunicorn` – python web server gateway 

## Project structure

- `/infra` – terraform code for network and infrastructure setup
- `/takemehome` – python module for API and client
- `/scripts` – bash and python scripts for deployment

---

# Development

## Setup

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirement.txt
pip install .
```

## Local Development

`python3 -m takemehome` – starts a local instance with sqlite
`python3 -m black` – PEP 8 format code

## Testing

`python3 -m unittest tests/test_api.py` – test app instance with sqlite


---

# Deployment

Manually execute `sudo sh scripts/setup.sh eth0:1 10.0.2.100 255.255.255.0`

1. Execute bash script for the following:
    1. Setup `venv` and python dependencies
    1. Update security context for `venv/{bin,lib}` 
    1. Run `bootstrap.py` for the one-time setup items
1. Setup sub-interface `eth0:1` with `10.0.2.100/24`.
    1. File created under `/etc/sysconfig/network-scripts`
1. Configure mysqld to listen only on `10.0.2.100`.
    1. Config file updated in `/etc/my.cnf.d/mysql-server.cnf`
1. Setup database user for connecting via `10.0.2.100` and permission for `tower` database.
1. Setup systemd service unit in `/etc/systemd/system/takemehome.service` for API service.

---

# Out of scope items

- CI/CD
- Resilience
- Security
- Monitoring

---

# Thank you! Questions?
