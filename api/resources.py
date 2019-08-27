from flask import Flask
from flask_restful import Api
from api.user import NewUser, User

app = Flask(__name__)
api = Api(app)


api.add_resource(User, "/api/user/<int:id>")
api.add_resource(User, "/api/users", endpoint='users')
api.add_resource(NewUser, '/api/new_user')
