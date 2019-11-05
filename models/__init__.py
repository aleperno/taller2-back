import os
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR
from utils import utcnow


DEFAULT_URL = 'postgresql+psycopg2://t2user:t2pass@localhost/t2db'
CONN_URL = os.environ.get('DATABASE_URL', DEFAULT_URL)
engine = create_engine(CONN_URL)
Session = scoped_session(sessionmaker(bind=engine))


class CommonBase(object):

    def save_to_db(self):
        Session.add(self)
        Session.commit()

    @classmethod
    def query(cls):
        return Session.query(cls)

    @classmethod
    def get_all(cls):
        return cls.query().all()

    @classmethod
    def get_all_dict(cls):
        return [r.as_dict() for r in cls.get_all()]

    @classmethod
    def get_by_id(cls, _id):
        return cls.query().get(_id)

    @classmethod
    def get_by_ids(cls, _ids):
        return cls.query().filter(cls.id.in_(_ids)).all()

    def as_dict(self):
        d = {}
        cols = [ c.name for c in self.__table__.columns ]
        for col in cols:
            value = getattr(self, col)
            if isinstance(value, datetime):
                d[col] = value.isoformat()
            else:
                d[col] = value
        return d


class JSONEncodedValue(TypeDecorator):  # pragma: no cover
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


Base = declarative_base(cls=CommonBase)
