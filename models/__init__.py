import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DEFAULT_URL = 'postgresql+psycopg2://t2user:t2pass@localhost/t2db'
CONN_URL = os.environ.get('DATABASE_URL', DEFAULT_URL)
engine = create_engine(CONN_URL)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
