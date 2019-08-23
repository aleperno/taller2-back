import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


DEFAULT_URL = 'postgresql+psycopg2://t2user:t2pass@localhost/t2db'
CONN_URL = os.environ.get('DATABASE_URL', DEFAULT_URL)
engine = create_engine(CONN_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class JSONEncodedValue(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class TallerUser(Base):
    __tablename__ = 't2table'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'age': self.age}

    def __repr__(self):
        return f'Taller 2 User. id: {self.id}, name: {self.name}, age: {self.age}'

Base.metadata.create_all(engine)

