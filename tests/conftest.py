import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

LOCAL_TEST_DB = 'postgresql://t2user:t2pass@localhost/t2db_test'
TEST_DB = os.environ.get('TEST_DB', LOCAL_TEST_DB)

engine = create_engine(TEST_DB)
Session = scoped_session(sessionmaker(bind=engine))

@pytest.fixture(scope='function')
def db_session():
    Base.metadata.create_all(engine)
    yield Session
    Session.close_all()
    Base.metadata.drop_all(bind=engine)
