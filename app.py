from flask import Flask
from flask import request
from flask_restful import Api

from backend_test.todo import Todo

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, "/todo/<int:id>")


aux = {
    "1": {"data": "Data one"},
    "2": {"data": "Data two"},
}

@app.route('/users/<user_id>', methods=['POST', 'GET', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        return aux[user_id], 200
    if request.method == 'POST':
        return request.data, 200


if __name__ == "__main__":
      app.run()
