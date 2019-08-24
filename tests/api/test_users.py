import json

def test_multiple_user(multiple_users, testing_app):
    r = testing_app.get('/api/users')
    assert r.status_code == 200
    assert r.json == [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'jdoe@gmail.com',
            'passwd': '12345'
        },
        {
            'id': 2,
            'name': 'Jane Doe',
            'email': 'janedoe@gmail.com',
            'passwd': '54321'
        }
    ]


def test_single_user(multiple_users, testing_app):
    r = testing_app.get('/api/user/1')
    assert r.status_code == 200
    assert r.json == {
        'id': 1,
        'name': 'John Doe',
        'email': 'jdoe@gmail.com',
        'passwd': '12345'
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
    r = testing_app.post(
        '/api/new_user',
        data=json.dumps({'name': 'Juancito', 'email': 'juancito@gmail.com', 'password': 'insecure'}),
        content_type='application/json'
    )
    assert r.status_code == 200
    assert r.json == {
        'id': 1,
        'name': 'Juancito',
        'email': 'juancito@gmail.com',
        'passwd': 'insecure'
    }


def test_user_existing_email(one_user, testing_app):
    r = testing_app.post(
        '/api/new_user',
        data=json.dumps({'name': 'Single User', 'email': 'suser@gmail.com', 'password': 'insecure'}),
        content_type='application/json'
    )

    assert r.status_code == 400
    assert r.json == 'Email already registered'

