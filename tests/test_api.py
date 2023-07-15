import unittest
import os
from flask import Flask
from takemehome.api import api
from takemehome.model import db

basedir = os.path.abspath(os.path.dirname(__file__))
test_db_path = os.path.join(basedir, "test.db")


def assert_response_json(want, got):
    assert got
    for i in range(len(got)):
        assert want[i].items() <= got[i].items()


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        if os.path.isfile(test_db_path):
            os.remove(test_db_path)
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + test_db_path
        db.init_app(app)
        api.init_app(app)
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        if os.path.isfile(test_db_path):
            os.remove(test_db_path)

    def test_swagger_generated(self):
        doc = self.client.get("/swagger.json")
        assert doc.json
        assert "basePath" in doc.json
        site = self.client.get("/")
        assert site.status_code == 200

    def test_empty_db(self):
        res = self.client.get("/show")
        assert res.json == []

    def test_create_then_update(self):
        invalid_entry = self.client.post("/create", json=dict())
        assert invalid_entry.status_code == 400
        first_entry = self.client.post(
            "/create", json=dict(username="a", message="first")
        )
        assert first_entry.status_code == 200
        second_entry = self.client.post(
            "/create", json=dict(username="b", message="second")
        )
        assert second_entry.status_code == 200
        res = self.client.get("/show")
        want = [
            dict(id=1, username="a", message="first"),
            dict(id=2, username="b", message="second"),
        ]
        assert_response_json(want, res.json)
        invalid_update = self.client.put("/update/10")
        assert invalid_update.status_code == 404
        update = self.client.put("/update/1", json=dict(username="c"))
        assert update.status_code == 200
        want_update = [
            dict(id=1, username="c", message="first"),
            dict(id=2, username="b", message="second"),
        ]
        assert_response_json(want_update, update.json)
