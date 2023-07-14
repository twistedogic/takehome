from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from .model import db, Entry

api = Api(title="takemehome", description="API connected to a database")


def get_entry_from_request(args) -> Entry:
    username, message = args.get("username", None), args.get("message", None)
    return Entry(username=username, message=message)


def list_all_entries(db: SQLAlchemy) -> list[dict[str, str]]:
    entries = db.session.execute(db.select(Entry).order_by(Entry.datetime)).scalars()
    return [e.to_dict() for e in entries]


@api.route("/show")
class ShowAll(Resource):
    def get(self):
        return list_all_entries(db)


create_parser = api.parser()
create_parser.add_argument(
    "username",
    location="json",
    type=str,
    required=True,
)
create_parser.add_argument(
    "message",
    location="json",
    type=str,
    required=True,
)


@api.route("/create")
class Create(Resource):
    @api.expect(create_parser)
    @api.response(400, "POST body validation error")
    @api.response(200, "Success")
    def post(self):
        args = create_parser.parse_args()
        entry = get_entry_from_request(args)
        db.session.add(entry)
        db.session.commit()
        return list_all_entries(db)


update_parser = api.parser()
update_parser.add_argument("username", location="json", type=str)
update_parser.add_argument("message", location="json", type=str)


@api.route("/update/<int:id>")
class Update(Resource):
    @api.expect(update_parser)
    @api.response(404, "Entry id not found")
    @api.response(200, "Success")
    def put(self, id: int):
        args = update_parser.parse_args()
        result = db.get_or_404(Entry, id, description=f"Entry with id {id} not found")
        entry = get_entry_from_request(args)
        if entry.username:
            result.username = entry.username
        if entry.message:
            result.message = entry.message
        db.session.commit()
        return list_all_entries(db)
