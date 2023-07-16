import argparse
import requests
from tabulate import tabulate


def print_response(json_data):
    if len(json_data) == 0:
        print("No entries returned")
    headers = [key for key in json_data[0].keys()]
    json_data.sort(key=lambda x: x.get("datetime", ""))
    rows = [[col for col in row.values()] for row in json_data]
    print(tabulate(rows, headers=headers))


class Client:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url

    def show(self):
        res = requests.get(self.base_url + "/show")
        if res.status_code == 200:
            print_response(res.json())
        res.raise_for_status()

    def create(self, username=None, message=None):
        if not username or not message:
            raise ValueError("username and message must be provided")
        res = requests.post(
            self.base_url + "/create", json=dict(username=username, message=message)
        )
        if res.status_code == 200:
            print_response(res.json())
        res.raise_for_status()

    def update(self, id, username=None, message=None):
        res = requests.put(
            self.base_url + "/update/" + id,
            json=dict(username=username, message=message),
        )
        if res.status_code == 200:
            print_response(res.json())
        res.raise_for_status()


parser = argparse.ArgumentParser(prog="client", description="CLI client for API")
parser.add_argument("--base_url", default="http://localhost:3000")
subparsers = parser.add_subparsers(dest="subcommand")
show_parser = subparsers.add_parser("show")
create_parser = subparsers.add_parser("create")
create_parser.add_argument("--username", required=True)
create_parser.add_argument("--message", required=True)
update_parser = subparsers.add_parser("update")
update_parser.add_argument("--id", required=True)
update_parser.add_argument("--username")
update_parser.add_argument("--message")


if __name__ == "__main__":
    args = parser.parse_args()
    client = Client(base_url=args.base_url)
    if args.subcommand == "show":
        client.show()
    if args.subcommand == "create":
        client.create(username=args.username, message=args.message)
    if args.subcommand == "update":
        client.update(args.id, username=args.username, message=args.message)
