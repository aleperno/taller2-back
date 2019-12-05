import pytest
import os
from copy import copy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from models.users import FoodieUser
from models.shops import FoodieShop, Product
from unittest.mock import PropertyMock
from api.admin_resources import app
from freezegun import freeze_time

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

BASIC_SHOP_DATA = {
    'name': 'Some Shop',
    'description': 'A description',
    'address': 'Avenida Siempreviva 742',
    'category': 'comida',
    'location': 'foo',
}

BASIC_PRODUCT_DATA = {
    'shop_id': 1,
    'name': 'Prod name',
    'description': 'desc producto',
    'category': 'comida',
    'price': 50
}


def get_dummy_user(**kw):
    data = copy(BASIC_USER_DATA)
    data.update(kw)
    return data


def get_dummy_shop(**kw):
    data = copy(BASIC_SHOP_DATA)
    data.update(kw)
    return data


def get_dummy_product(**kw):
    data = copy(BASIC_PRODUCT_DATA)
    data.update(kw)
    return data


@pytest.fixture(scope='function')
def db_session(mocker):
    Base.metadata.create_all(engine)
    mocked_session = PropertyMock(return_value=Session)
    mocker.patch('models.Session', new_callable=mocked_session)
    # mocker.patch('models.create_engine', return_value=engine)
    yield Session
    Session.close_all()
    # Session().close_all_sessions()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def testing_app():
    return app.test_client()


@pytest.fixture
@freeze_time("2019-09-28 13:48:00")
def one_user(db_session):
    user_data = get_dummy_user(name='Single', surname='User', email='suser@gmail.com')
    user = FoodieUser(id=1, **user_data)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
@freeze_time("2019-09-28 13:48:00")
def multiple_users(db_session):
    data1 = get_dummy_user(name='John', surname='Doe', email='jdoe@gmail.com')
    data2 = get_dummy_user(name='Jane', surname='Doe', email='janedoe@gmail.com')
    user1 = FoodieUser(id=1, **data1)
    user2 = FoodieUser(id=2, **data2)
    db_session.add_all([user1, user2])
    db_session.commit()


@pytest.fixture
@freeze_time("2019-09-28 13:48:00")
def loaded_data(db_session):
    # Agrego Usuarios
    user1 = get_dummy_user(name='User1', surname='Perez', email='user1@gmail.com')
    user2 = get_dummy_user(name='User2', surname='Perez', email='user2@gmail.com')
    user3 = get_dummy_user(name='User3', surname='Perez', email='user3@gmail.com')
    deli1 = get_dummy_user(name='Deli1', surname='Perez', email='deli1@gmail.com', role='delivery')
    deli2 = get_dummy_user(name='Deli2', surname='Perez', email='deli2@gmail.com', role='delivery')
    deli3 = get_dummy_user(name='Deli3', surname='Perez', email='deli3@gmail.com', role='delivery')
    data = [user1, user2, user3, deli1, deli2, deli3]
    users = [FoodieUser(**d) for d in data]
    db_session.add_all(users)
    db_session.commit()

    # Agrego Shops
    shop1 = FoodieShop(**get_dummy_shop(name='Shop1'))
    shop2 = FoodieShop(**get_dummy_shop(name='Shop2'))
    shop3 = FoodieShop(**get_dummy_shop(name='Shop3'))
    db_session.add_all([shop1, shop2, shop3])
    db_session.commit()

    # Agrego Productos
    prod1 = Product(**get_dummy_product(shop_id=1, name='prod1', price='10'))
    prod2 = Product(**get_dummy_product(shop_id=1, name='prod1', price='10'))
    prod3 = Product(**get_dummy_product(shop_id=2, name='prod1', price='10'))
    # El shop 3 no tiene productos
    db_session.add_all([prod1, prod2, prod3])

    db_session.commit()