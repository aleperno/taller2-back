import json


def test_facebook_login(testing_app, one_user, mocker):
    mocker.patch('models.users.random_string', return_value='apptoken')
    fb_validator = mocker.patch('api.auth.facebook_get_email', return_value=one_user.email)
    json_body = {'fb_access_token': 'fbtoken'}

    r = testing_app.post(
        '/api/fb_login',
        data=json.dumps(json_body),
    )

    assert r.status_code == 200
    assert r.json == {'token': f'{one_user.id}.apptoken'}
    fb_validator.assert_called_once_with('fbtoken')


def test_facebook_login_bad_token(testing_app, mocker):
    mocker.patch('api.auth.facebook_get_email', return_value=None)
    json_body = {'fb_access_token': 'fbtoken'}

    r = testing_app.post(
        '/api/fb_login',
        data=json.dumps(json_body),
    )

    assert r.status_code == 400
    assert r.json == 'Token invalido'


def test_facebook_token_inexistente_email(testing_app, db_session, mocker):
    mocker.patch('api.auth.facebook_get_email', return_value='fooo@bar.com')
    json_body = {'fb_access_token': 'fbtoken'}

    r = testing_app.post(
        '/api/fb_login',
        data=json.dumps(json_body),
    )

    assert r.status_code == 404
    assert r.json == 'Usuario inexistente'


def test_facebook_no_token_json(testing_app):
    r = testing_app.post('/api/fb_login', data=json.dumps({}))

    assert r.status_code == 400
    assert r.json == {'fb_access_token': ['Missing data for required field.']}
