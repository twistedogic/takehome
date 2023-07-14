from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
        "Field1", db.DateTime(timezone=True), default=datetime.utcnow()
    )
    username = db.Column("Field2", db.Text, nullable=False)
    message = db.Column("Field3", db.Text, nullable=False)

    def to_dict(self) -> dict[str, str]:
        return dict(
            id=self.id,
            datetime=self.datetime.isoformat(),
            username=self.username,
            message=self.message,
        )
