import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base, GlovoUser
from unittest.mock import PropertyMock
from api.resources import app

LOCAL_TEST_DB = 'postgresql://t2user:t2pass@localhost/t2db_test'
TEST_DB = os.environ.get('TEST_DB', LOCAL_TEST_DB)

engine = create_engine(TEST_DB)
Session = scoped_session(sessionmaker(bind=engine))

@pytest.fixture(scope='function')
def db_session(mocker):
    Base.metadata.create_all(engine)
    mocked_session = PropertyMock(return_value=Session)
    mocker.patch('models.Session', new_callable=mocked_session)
    yield Session
    Session.close_all()
    #Session().close_all_sessions()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def testing_app():
    return app.test_client()


@pytest.fixture
def one_user(db_session):
    user = GlovoUser(id=1, name='Single', surname='User', email='suser@gmail.com', password='12345')
    db_session.add(user)
    db_session.commit()


@pytest.fixture
def multiple_users(db_session):
    user1 = GlovoUser(id=1, name='John', surname='Doe', email='jdoe@gmail.com', password='12345')
    user2 = GlovoUser(id=2, name='Jane', surname='Doe', email='janedoe@gmail.com', password='54321')
    db_session.add_all([user1, user2])
    db_session.commit()
