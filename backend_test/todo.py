from flask_restful import Resource
from flask import request, Flask
from flask_restful import Api


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


