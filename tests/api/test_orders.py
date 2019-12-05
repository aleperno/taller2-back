import pytest
import json
from models.deliveries import DeliveryStatus
from models.users import FoodieUser
from freezegun import freeze_time


@pytest.fixture
def mock_order_distance(mocker):
    mocker.patch('models.shops.distance_between', return_value=[{'distance': 1500}])


@pytest.fixture
def mocked_order_selected_delivery(mocker, loaded_data, testing_app, mock_order_distance, db_session):
    dummy_data = [
        {'status': True, 'distance': 1000},
    ]
    mocker.patch('models.deliveries.distance_between', return_value=dummy_data)
    del1 = DeliveryStatus(user_id=4, location='Fooo', available=True)
    db_session.add(del1)
    db_session.commit()

    pricing = mocker.patch('api.shops.PricingEngine')
    pricing.get_distance_price.return_value = 444
    body = {
        "user_id": 1,
        "shop_id": 1,
        "user_location": "-34.572259,-58.4843497",
        "products": [{"id": 1, "quantity": 1}],
        "favor": False
    }

    r = testing_app.post(
        '/api/orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 200

    body = {
        "user_id": 1,
        "order_id": 1,
        "delivery_id": 4
    }
    r = testing_app.post(
        '/api/orders/choose_delivery',
        data=json.dumps(body),
        content_type='application/json'
    )
    assert r.status_code == 200


def test_order_no_deliveries(mocker, loaded_data, testing_app, mock_order_distance):
    #mocker.patch('models.deliveries.distance_between')
    pricing = mocker.patch('api.shops.PricingEngine')
    pricing.get_distance_price.return_value = 444
    body = {
        "user_id": 1,
        "shop_id": 1,
        "user_location": "-34.572259,-58.4843497",
        "products": [{"id": 1, "quantity": 1}],
        "favor": False
    }

    r = testing_app.post(
        '/api/orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 200
    assert r.json == {
        "order_id": 1,
        "available": [],
        "closest": None,
        "delivery_price": 444,
        "order_price": 10
    }


def test_delivery_set_available(mocker, loaded_data, testing_app):
    # Initial Status
    assert not DeliveryStatus.get_all_available()

    # Setup
    body = {
        'user_id': 4,
        'location': '-34.55,-45.33',
        'available': True,
    }

    r = testing_app.post(
        '/api/deliveries/status',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 201

    # Assert after
    available = DeliveryStatus.get_all_available()
    assert len(available) == 1
    assert available[0].user_id == 4


@freeze_time("2019-09-28 13:48:00")
def test_order_two_deliveries(mocker, loaded_data, testing_app, mock_order_distance, db_session):
    dummy_data = [
        {'status': True, 'distance': 1000},
        {'status': True, 'distance': 1500},
    ]
    mocker.patch('models.deliveries.distance_between', return_value=dummy_data)
    del1 = DeliveryStatus(user_id=4, location='Fooo', available=True)
    del2 = DeliveryStatus(user_id=5, location='Fooo', available=True)
    db_session.add_all([del1, del2])
    db_session.commit()

    pricing = mocker.patch('api.shops.PricingEngine')
    pricing.get_distance_price.return_value = 444
    body = {
        "user_id": 1,
        "shop_id": 1,
        "user_location": "-34.572259,-58.4843497",
        "products": [{"id": 1, "quantity": 1}],
        "favor": False
    }

    r = testing_app.post(
        '/api/orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 200
    expected = {
        "order_id": 1,
        "available": [
            {
                'user_id': 4,
                'location': 'Fooo',
                'available': True,
                'name': 'Deli1',
                'surname': 'Perez',
                'reputation': None,
                'distance': 1000,
                'last_updated': '2019-09-28T13:48:00',
            },
            {
                'user_id': 5,
                'location': 'Fooo',
                'available': True,
                'name': 'Deli2',
                'surname': 'Perez',
                'reputation': None,
                'distance': 1500,
                'last_updated': '2019-09-28T13:48:00',
            }
        ],
        "closest": 4,
        "delivery_price": 444,
        "order_price": 10
    }
    assert r.json == expected

    # Consulto el estado con la API de status

    r = testing_app.get('/api/orders/1/status')
    assert r.status_code == 200
    expected.pop('order_id')
    expected.update({
        "status_id": 0,
        "status": "pending"
    })

    assert r.json == expected


@freeze_time("2019-09-28 13:48:00")
def test_choose_delivery(mocker, loaded_data, testing_app, mock_order_distance, db_session):
    dummy_data = [
        {'status': True, 'distance': 1000},
        {'status': True, 'distance': 1500},
    ]
    mocker.patch('models.deliveries.distance_between', return_value=dummy_data)
    del1 = DeliveryStatus(user_id=4, location='Fooo', available=True)
    del2 = DeliveryStatus(user_id=5, location='Fooo', available=True)
    db_session.add_all([del1, del2])
    db_session.commit()

    pricing = mocker.patch('api.shops.PricingEngine')
    pricing.get_distance_price.return_value = 444
    body = {
        "user_id": 1,
        "shop_id": 1,
        "user_location": "-34.572259,-58.4843497",
        "products": [{"id": 1, "quantity": 1}],
        "favor": False
    }

    r = testing_app.post(
        '/api/orders',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 200

    # HASTA ACA IGUAL AL TEST ANTERIOR

    body = {
        "user_id": 1,
        "order_id": 1,
        "delivery_id": 4
    }

    r = testing_app.post(
        '/api/orders/choose_delivery',
        data=json.dumps(body),
        content_type='application/json'
    )

    assert r.status_code == 200
    assert r.json == {
        "status_id": 1,
        "status": "Waiting delivery acceptance"
    }


def test_delivery_accept_order_no_orders(mocked_order_selected_delivery, testing_app):
    # El delivery 5 no posee ordenes para aceptar
    r = testing_app.get('/api/orders/available/5')

    assert r.status_code == 200
    assert r.json == []


def test_delivery_accept_order(mocked_order_selected_delivery, testing_app):
    # El delivery 4 posee una orden para aceptar
    r = testing_app.get('/api/orders/available/4')

    assert r.status_code == 200
    assert r.json == [
        {
            'id': 1,
            'shop_id': 1,
            'user_id': 1,
            'user_location': "-34.572259,-58.4843497",
            'shop_location': 'foo',
            'distance': 1500,
            'favor': False,
            'products': [{'id': 1, 'quantity': 1}],
            'address': None,
            'distance_to_shop': 1000,
            'total_distance': 2500,
            'user_data': {'name': 'User1', 'surname': 'Perez', 'reputation': None},
            'revenue': 377.4 # .85 * 444
        }
    ]

    # Acepto la orden
    r = testing_app.put('/api/orders/available/4', data=json.dumps({'status': 'accepted', 'order_id': 1}))

    assert r.status_code == 200
    assert r.json is True

    # Valido que la orden cambio de estado

    r = testing_app.get('/api/orders/1/status')

    assert r.status_code == 200
    assert r.json == {
        'delivery_data': {
            'name': 'Deli1',
            'reputation': None,
            'surname': 'Perez'
        },
        'delivery_location': 'Fooo',
        'status_id': 2,
        'status': 'accepted'
    }

    testing_app.put('/api/orders/available/4', data=json.dumps({'status': 'in_shop', 'order_id': 1}))
    testing_app.put('/api/orders/available/4', data=json.dumps({'status': 'out_shop', 'order_id': 1}))
    testing_app.put('/api/orders/available/4', data=json.dumps({'status': 'delivered', 'order_id': 1}))

    r = testing_app.post('/api/orders/confirm', data=json.dumps({'user_id': 1, 'order_id': 1}))

    assert r.status_code == 200

    user = FoodieUser.get_by_id(1)
    deli = FoodieUser.get_by_id(4)

    assert user.cash_balance == -444
    assert deli.cash_balance == 377.4

