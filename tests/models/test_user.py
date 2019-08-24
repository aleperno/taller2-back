import pytest
from models import GlovoUser


def test_one_user(one_user, db_session):
    user = db_session.query(GlovoUser).get(1)
    assert user.as_dict() == {'id': 1, 'name': 'Single User', 'email': 'suser@gmail.com', 'passwd': '12345'}


def test_no_user(db_session):
    assert not db_session.query(GlovoUser).all()