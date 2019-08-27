import json
import pytest


def test_multiple_user(multiple_users, testing_app):
    r = testing_app.get('/api/users')
    assert r.status_code == 200
    assert r.json == [
        {
            'id': 1,
            'name': 'John',
            'surname': 'Doe',
            'email': 'jdoe@gmail.com',
            'password': 'insecure',
            'phone': '4444-5555',
            'subscription': 'flat',
            'role': 'user'
        },
        {
            'id': 2,
            'name': 'Jane',
            'surname': 'Doe',
            'email': 'janedoe@gmail.com',
            'password': 'insecure',
            'phone': '4444-5555',
            'subscription': 'flat',
            'role': 'user'
        }
    ]


def test_single_user(multiple_users, testing_app):
    r = testing_app.get('/api/user/1')
    assert r.status_code == 200
    assert r.json == {
        'id': 1,
        'name': 'John',
        'surname': 'Doe',
        'email': 'jdoe@gmail.com',
        'password': 'insecure',
        'phone': '4444-5555',
        'subscription': 'flat',
        'role': 'user'
    }


def test_single_nonexistent_user(multiple_users, testing_app):
    r = testing_app.get('/api/user/999')
    assert r.status_code == 404
    assert r.json == 'User with id 999 was not found'


def test_no_user(db_session, testing_app):
    r = testing_app.get('/api/users')
    assert r.status_code == 200
    assert r.json == []


def test_new_user(db_session, testing_app):
    # Assert initial status
    assert testing_app.get('/api/users').json == []

    # Setup
    json_body = {
        'name': 'Juancito',
        'surname': 'Lopez',
        'email': 'juancito@gmail.com',
        'password': 'insecure',
        'phone': '4781-6140'
    }

    r = testing_app.post(
        '/api/new_user',
        data=json.dumps(json_body),
        content_type='application/json'
    )
    assert r.status_code == 201
    assert r.json == {
        'id': 1,
        'name': 'Juancito',
        'surname': 'Lopez',
        'email': 'juancito@gmail.com',
        'password': 'insecure',
        'phone': '4781-6140',
        'subscription': 'flat',
        'role': 'user'

    }


def test_user_existing_email(one_user, testing_app):
    json_body = {
        'name': 'Single',
        'surname': 'User',
        'email': 'suser@gmail.com',
        'password': 'insecure',
        'phone': '4444-5555'
    }
    r = testing_app.post(
        '/api/new_user',
        data=json.dumps(json_body),
        content_type='application/json'
    )

    assert r.status_code == 400
    assert r.json == {'email': ['Email already exists']}


def test_login_existing_user(mocker, one_user, testing_app):
    mocker.patch('models.users.random_string', return_value='abcdedcba')
    json_body = {
        'email': 'suser@gmail.com',
        'password': 'insecure'
    }
    r = testing_app.post(
        '/api/login',
        data=json.dumps(json_body),
    )
    assert r.status_code == 200
    assert r.json == {'token': f'{one_user.id}.abcdedcba'}

    # Secuential calls should return the same

    r = testing_app.post(
        '/api/login',
        data=json.dumps(json_body),
    )
    assert r.status_code == 200
    assert r.json == {'token': f'{one_user.id}.abcdedcba'}


def test_login_nonexistent_user(db_session, testing_app):
    json_body = {
        'email': 'nobody@gmail.com',
        'password': 'asdqwer'
    }
    r = testing_app.post(
        '/api/login',
        data=json.dumps(json_body),
    )
    assert r.status_code == 404
    assert r.json == 'User not found'


def test_login_wrong_password(one_user, testing_app):
    json_body = {
        'email': 'suser@gmail.com',
        'password': 'thisisnotthepassword'
    }
    r = testing_app.post(
        '/api/login',
        data=json.dumps(json_body),
    )
    assert r.status_code == 401
    assert r.json == 'Wrong Password'


@pytest.mark.parametrize('missing', ('email', 'password'))
def test_login_missing_field(missing, testing_app):
    json_body = {
        'email': 'suser@gmail.com',
        'password': 'thisisnotthepassword'
    }
    json_body.pop(missing)
    r = testing_app.post(
        '/api/login',
        data=json.dumps(json_body),
    )
    assert r.status_code == 400
    assert r.json == {missing: ['Missing data for required field.']}
