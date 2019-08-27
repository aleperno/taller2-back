import pytest
import os
from copy import copy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from models.users import FoodieUser
from unittest.mock import PropertyMock
from api.resources import app

LOCAL_TEST_DB = 'postgresql://t2user:t2pass@localhost/t2db_test'
TEST_DB = os.environ.get('TEST_DB', LOCAL_TEST_DB)

engine = create_engine(TEST_DB)
Session = scoped_session(sessionmaker(bind=engine))

BASIC_USER_DATA = {
    'name': 'John',
    'surname': 'Doe',
    'phone': '4444-5555',
    'email': 'jdoe@gmail.com',
    'subscription': 'flat',
    'role': 'user',
    'password': 'insecure'
}


def get_dummy_user(**kw):
    data = copy(BASIC_USER_DATA)
    data.update(kw)
    return data


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
    user_data = get_dummy_user(name='Single', surname='User', email='suser@gmail.com')
    user = FoodieUser(id=1, **user_data)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def multiple_users(db_session):
    data1 = get_dummy_user(name='John', surname='Doe', email='jdoe@gmail.com')
    data2 = get_dummy_user(name='Jane', surname='Doe', email='janedoe@gmail.com')
    user1 = FoodieUser(id=1, **data1)
    user2 = FoodieUser(id=2, **data2)
    db_session.add_all([user1, user2])
    db_session.commit()
