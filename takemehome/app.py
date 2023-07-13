from flask import Flask, request, Request, abort, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Entry(db.Model):
    """
    This describes the model with SQL table 'tower'
        id INTEGER NOT NULL,
        "Field1" DATETIME DEFAULT (CURRENT_TIMESTAMP),
        "Field2" TEXT NOT NULL,
        "Field3" TEXT NOT NULL,
        PRIMARY KEY (id)
    """

    __tablename__ = "tower"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(
        "Field1", db.DateTime(timezone=True), server_default=func.now()
    )
    username = db.Column("Field2", db.Text, nullable=False)
    message = db.Column("Field3", db.Text, nullable=False)

    def to_dict(self) -> dict[str, str]:
        return dict(
            id=self.id,
            datetime=self.datetime,
            username=self.username,
            message=self.message,
        )

    def is_valid(self) -> bool:
        return self.username and self.message


def get_entry_from_request(req: Request) -> Entry:
    args = req.args
    username, message = args.get("username", None), args.get("message", None)
    if req.method == "POST":
        form = request.form
        username, message = form.get("username", None), form.get("username", None)
    return Entry(username=username, message=message)


def list_all_entries(db: SQLAlchemy) -> list[dict[str, str]]:
    entries = db.session.execute(db.select(Entry).order_by(Entry.datetime)).scalars()
    return [e.to_dict() for e in entries]


@app.route("/")
def menu() -> str:
    return """<ul>
<li>/ - show all path</li>
<li>/show - list all entries from table</li>
<li>/create - create new entry to table</li>
<li>/update/:id - update entry</li>
</ul>
"""


@app.route("/show", methods=["GET"])
def show_all() -> list[dict[str, str]]:
    return list_all_entries(db)


@app.route("/create", methods=["GET", "POST"])
def create():
    entry = get_entry_from_request(request)
    if not entry.is_valid():
        abort(400)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("show_all"))


@app.route("/update/<int:id>", methods=["GET", "PUT", "POST"])
def update(id: int):
    result = db.get_or_404(Entry, id)
    entry = get_entry_from_request(request)
    if entry.username:
        result.username = entry.username
    if entry.message:
        result.message = entry.message
    db.session.commit()
    return redirect(url_for("show_all"))
