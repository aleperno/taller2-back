from flask_restful import Resource
from flask import request, Flask
from flask_restful import Api
from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import sessionmaker
import models
from models import GlovoUser



class User(Resource):
    def get(self, id=None):
        if id is None:
            r = models.Session.query(GlovoUser).all()
            return [e.as_dict() for e in r], 200
        else:
            r = models.Session.query(GlovoUser).get(id)
            if r is not None:
                return r.as_dict(), 200
            else:
                return f"User with id {id} was not found", 404
