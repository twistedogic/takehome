import os
import subprocess
import argparse
import ipaddress

default_mysql_config_path = "/etc/my.cnf.d/mysql-server.cnf"
default_network_scripts_path = "/etc/sysconfig/network-scripts"
default_systemd_unit_path = "/etc/systemd/system/takemehome.service"
default_system_user = "rocky"
default_database = "tower"

ifcfg_template = """# setup by takemehome bootstrap
BOOTPROTO=none
DEVICE={name}
ONBOOT=yes
TYPE=Ethernet
IPADDR={ip}
NETMASK={mask}
"""

sql_setup_template = """CREATE USER IF NOT EXISTS {username}@{ip};
GRANT ALL PRIVILEGES ON {database}.* TO {username}@{ip};
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS {database};"""

systemd_unit_template = """[Unit]
Description=API service
After=network.target

[Service]
User={user}
WorkingDirectory={dir}
Environment=FLASK_CONFIG=production
Environment=SQLALCHEMY_DATABASE_URI=mysql+pymysql://{username}@{ip}/{database}
ExecStart={venv}/bin/gunicorn -b 0.0.0.0:3000 -w 4 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target"""


def read_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        return content


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


def run_cmd(cmd):
    subprocess.run(cmd, shell=True)


def setup_sub_interface(name, ip, mask, dir=default_network_scripts_path):
    filename = "ifcfg-{name}".format(name=name)
    content = ifcfg_template.format(name=name, ip=ip, mask=mask)
    write_file(os.path.join(dir, filename), content)
    run_cmd("systemctl restart NetworkManager")


def bind_sql_address(ip, config_path=default_mysql_config_path):
    content = read_file(config_path)
    lines = content.split("\n") + []
    address_set = False
    for i, line in enumerate(lines):
        if line.startswith("bind-address"):
            lines[i] = "bind-address={ip}".format(ip=ip)
            address_set = True
            break
    if not address_set:
        lines.append("bind-address={ip}".format(ip=ip))
    write_file(config_path, "\n".join(lines))
    run_cmd("systemctl restart mysqld.service")


def setup_database(ip, username, database=default_database):
    stmt = sql_setup_template.format(ip=ip, username=username, database=database)
    run_cmd('mysql -u root -e "{}"'.format(stmt))


def setup_api(
    db_user, ip, dir, venv, database=default_database, user=default_system_user
):
    clean_dir, clean_venv = os.path.abspath(dir), os.path.abspath(venv)
    unit = systemd_unit_template.format(
        username=db_user,
        ip=ip,
        database=database,
        venv=clean_venv,
        dir=clean_dir,
        user=user,
    )
    write_file(default_systemd_unit_path, unit)
    run_cmd("systemctl daemon-reload")
    run_cmd("systemctl start takemehome.service")
    run_cmd("systemctl enable takemehome.service")


def validate_ip_v4(ip):
    ipaddress.IPv4Address(ip)


def validate_dir_path(path):
    if not os.path.isdir(path):
        raise ValueError("{} is not found".format(path))


parser = argparse.ArgumentParser(
    prog="bootstrap",
    description="""
        Setup subinterface, mysql server and systemd service unit for API
        """,
)
parser.add_argument("name", help="subinterface name")
parser.add_argument("ip", help="IP address for subinterface")
parser.add_argument("mask", help="netmask for subinterface", default="255.255.255.0")
parser.add_argument("--db_user", help="database user", default="tower")
parser.add_argument("--venv", help="virtualenv path", required=True)
parser.add_argument("--dir", help="App home directory", required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    validate_ip_v4(args.ip)
    validate_ip_v4(args.mask)
    validate_dir_path(args.venv)
    validate_dir_path(args.dir)
    setup_sub_interface(args.name, args.ip, args.mask)
    print("complete subinterface setup")
    bind_sql_address(args.ip)
    setup_database(args.ip, args.db_user)
    print("complete myql setup")
    setup_api(args.db_user, args.ip, args.dir, args.venv)
    print("complete api setup")
