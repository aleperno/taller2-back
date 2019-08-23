from flask_restful import Resource
from flask import request, Flask
from flask_restful import Api
from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import sessionmaker

from models import Session, GlovoUser

s = Session()

todos = {
    1: {
        "id": 1,
        "item": "Create sample app",
        "status": "Completed"
        },
    2:  {
        "id": 2,
        "item": "Deploy in Heroku",
        "status": "Open"
        },
    3:  {
        "id": 3,
        "item": "Publish",
        "status": "Open"
        },
}


class Todo(Resource):
    def get(self, id=None):
        if id is None:
            return todos, 200
        else:
            todo = todos.get(id, None)
            if todo is not None:
                return todo, 200
            return "Item not found for the id: {}".format(id), 404

    def put(self, id):
        import pdb; pdb.set_trace()
        todos[id] = request.form['data']
        return todos[id], 200


class User(Resource):
    def get(self, id=None):
        if id is None:
            r = s.query(GlovoUser).all()
            return [e.as_dict() for e in r], 200
        else:
            r = s.query(GlovoUser).get(id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"Item with id {id} was not found", 404
