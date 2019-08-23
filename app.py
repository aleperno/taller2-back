from flask import Flask
from flask import request
from flask_restful import Api

from api.todo import Todo, User

app = Flask(__name__)
api = Api(app)


api.add_resource(Todo, "/api/todo/<int:id>")
api.add_resource(Todo, "/api/todos", endpoint='todos')
api.add_resource(User, "/api/user/<int:id>")
api.add_resource(User, "/api/users", endpoint='users')


if __name__ == "__main__":
    app.run()
