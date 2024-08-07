import os
from typing import cast

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
password = os.environ.get("PASSWORD")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://joe:{password}@localhost:5432/example"
)
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Person ID: {self.id}, name: {self.name}>"


db.create_all()


@app.route("/")
def index():
    person = cast(Person, Person.query.first())
    return "Hello " + person.name


if __name__ == "__main__":
    app.run()
