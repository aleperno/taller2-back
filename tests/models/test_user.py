from models.users import FoodieUser


def test_one_user(one_user, db_session):
    user = db_session.query(FoodieUser).get(1)
    assert user.as_dict() == {'id': 1,
                              'name': 'Single',
                              'surname': 'User',
                              'email': 'suser@gmail.com',
                              'phone': '4444-5555',
                              'password': 'insecure',
                              'subscription': 'flat',
                              'role': 'user',
                              'photo_url': None,
                              'creation_date': '2019-09-28T13:48:00',
                              'status': 'active',
                              'active': True,
                              'cash_balance': 0,
                              'favor_balance': 0,
                              }


def test_no_user(db_session):
    assert not db_session.query(FoodieUser).all()
