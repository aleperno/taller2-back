import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

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
    def get_all(self):
        return [r.as_dict() for r in self.query().all()]

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



Base = declarative_base(cls=CommonBase)
