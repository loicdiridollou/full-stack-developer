import os
import sys

from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   url_for)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
password = os.environ.get("PASSWORD")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://udacity:{password}@localhost:5432/todoapp"
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("todolists.id"), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"


class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship("Todo", backref="list", lazy=True)


@app.route("/todos/create", methods=["POST"])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()["description"]
        list_id = request.get_json()["list_id"]
        todo = Todo(description=description, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body["description"] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)


@app.route("/lists/create", methods=["POST"])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()["list_name"]
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body["name"] = todolist.name
        body["id"] = todolist.id
        print(todolist.name)
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)


@app.route("/todos/<todo_id>/set-completed", methods=["POST"])
def set_todos_completed(todo_id):
    try:
        completed = request.get_json(force=True)["completed"]
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for("index"))


@app.route("/todos/<todo_id>/delete", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({"success": True})


@app.route("/lists/<list_id>/delete", methods=["DELETE"])
def delete_list(list_id):
    error = False
    try:
        lists = TodoList.query.get(list_id)
        for todo in lists.todos:
            db.session.delete(todo)

        db.session.delete(lists)
        db.session.commit()
    except ():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({"success": True})


@app.route("/lists/<list_id>")
def get_list_todo(list_id):
    return render_template(
        "index.html",
        todos=Todo.query.filter_by(list_id=list_id).order_by("id").all(),
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
    )


@app.route("/")
def index():
    return redirect(url_for("get_list_todo", list_id=1))


if __name__ == "__main__":
    app.run()
