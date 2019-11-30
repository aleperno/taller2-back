import json
import pytest
from freezegun import freeze_time
from datetime import datetime, timedelta
from models.users import PasswordRecoveryToken


@freeze_time("2019-09-28 13:48:00")
def test_multiple_user(multiple_users, testing_app):
    r = testing_app.get('/api/admin/users')
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
            'role': 'user',
            'photo_url': None,
            'creation_date': '2019-09-28T13:48:00',
            'status': 'active',
            'active': True,
        },
        {
            'id': 2,
            'name': 'Jane',
            'surname': 'Doe',
            'email': 'janedoe@gmail.com',
            'password': 'insecure',
            'phone': '4444-5555',
            'subscription': 'flat',
            'role': 'user',
            'photo_url': None,
            'creation_date': '2019-09-28T13:48:00',
            'status': 'active',
            'active': True,
        }
    ]


@freeze_time("2019-09-28 13:48:00")
def test_single_user(multiple_users, testing_app):
    r = testing_app.get('/api/admin/users/1')
    assert r.status_code == 200
    assert r.json == {
        'id': 1,
        'name': 'John',
        'surname': 'Doe',
        'email': 'jdoe@gmail.com',
        'password': 'insecure',
        'phone': '4444-5555',
        'subscription': 'flat',
        'role': 'user',
        'photo_url': None,
        'creation_date': '2019-09-28T13:48:00',
        'status': 'active',
        'active': True,
    }


def test_single_nonexistent_user(multiple_users, testing_app):
    r = testing_app.get('/api/admin/users/999')
    assert r.status_code == 404
    assert r.json == 'User with id 999 was not found'


def test_no_user(db_session, testing_app):
    r = testing_app.get('/api/admin/users')
    assert r.status_code == 200
    assert r.json == []


@freeze_time("2019-09-28 13:48:00")
def test_new_user(db_session, testing_app):
    """
    Tests the creation of a new user through the API and the server's response
    """
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
        'role': 'user',
        'photo_url': None,
        'creation_date': '2019-09-28T13:48:00',
        'status': 'active',
        'active': True,
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


@freeze_time("2019-09-28 13:48:12")
def test_forgot_password(mocker, one_user, testing_app):
    send_mail = mocker.patch('api.auth.send_token_to_mail')
    mocker.patch('models.users.random_string', return_value="abcdDCBA")
    json_body = {
        'email': 'suser@gmail.com',
    }
    r = testing_app.post(
        '/api/forgot_password',
        data=json.dumps(json_body),
    )
    assert r.status_code == 200
    send_mail.assert_called_once_with('abcdDCBA',
                                      one_user.email,
                                      datetime.utcnow()+timedelta(days=1))


@pytest.mark.parametrize("email", (None, 'foo@gmail.com', 'sarasa'))
def test_forgot_password_error(one_user, testing_app, email):
    """
    Tests for errors in the Forgot Password API
     - Missing email field
     - Non-existent mail
     - invalid mail format
    """
    json_body = {}
    if email:
        json_body['email'] = email

    r = testing_app.post(
        '/api/forgot_password',
        data=json.dumps(json_body),
    )

    assert r.status_code == 400


def test_reset_password(one_user, testing_app):
    token = PasswordRecoveryToken.generate_token(one_user.id)
    new_password = '123456'
    assert one_user.password != new_password
    assert token.valid is True
    json_body = {
        'email': one_user.email,
        'token': token.token,
        'password': new_password,
        'confirm_password': new_password
    }
    r = testing_app.post(
        '/api/reset_password',
        data=json.dumps(json_body),
    )
    assert r.status_code == 200
    assert r.json == 'Password Changed'

    assert token.valid is False  # Token Cannot be reused
    assert one_user.password == new_password  # User password changed
