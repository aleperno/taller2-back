import pytest
from models import GlovoUser

@pytest.fixture
def one_user(db_session):
    user = GlovoUser(name='John Doe', email='jdoe@gmail.com', password='12345')
    db_session.add(user)
    db_session.commit()


def test_one_user(one_user, db_session):
    user = db_session.query(GlovoUser).filter(GlovoUser.email=='jdoe@gmail.com').scalar()
    assert user.as_dict() == {'id': 1, 'name': 'John Doe', 'email': 'jdoe@gmail.com', 'passwd': '12345'}
