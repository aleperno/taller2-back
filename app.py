from flask import Flask
from flask import request
from flask_restful import Api

from backend_test.todo import Todo, User

app = Flask(__name__)
api = Api(app)


api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Todo, "/todos", endpoint='todos')
api.add_resource(User, "/user/<int:id>")
api.add_resource(User, "/users", endpoint='users')


if __name__ == "__main__":
      app.run()
