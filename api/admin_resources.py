from api.resources import api, app
from api.admin.users import ListUsers

api.add_resource(ListUsers, "/api/admin/users/<int:user_id>")
api.add_resource(ListUsers, "/api/admin/users", endpoint='users')