import pytest


def test_get_shops(loaded_data, testing_app):
    """
    Pruebo que se cargue bien la info de los shops.
    Asímismo que si un shop no tiene productos (como el shop3) no figure en el resultado.
    """
    r = testing_app.get('/api/shops')

    assert r.status_code == 200

    data = r.json

    assert data == [
        {
            'id': 1,
            'name': 'Shop1',
            'description': 'A description',
            'address': 'Avenida Siempreviva 742',
            'location': None,
            'category': 'comida',
            'creation_date': '2019-09-28T13:48:00',
            'active': True,
            'location': 'foo',
        },
        {
            'id': 2,
            'name': 'Shop2',
            'description': 'A description',
            'address': 'Avenida Siempreviva 742',
            'location': None,
            'category': 'comida',
            'creation_date': '2019-09-28T13:48:00',
            'active': True,
            'location': 'foo',
        }
    ]


def no_test_shop_products(loaded_data, testing_app):
    r = testing_app.get('/api/shops/1/products')

    assert r.status_code == 200
    assert len(r.json) == 2
    assert r.json == [
        {
            'id': 1,
            'shop_id': 1,
            'name': 'prod1',
            'description': 'desc producto',
            'category': 'comida',
            'price': 10.0,
            'creation_date': '2019-09-28T13:48:00',
            'active': True
        },
        {
            'id': 2,
            'shop_id': 1,
            'name': 'prod1',
            'description': 'desc producto',
            'category': 'comida',
            'price': 10.0,
            'creation_date': '2019-09-28T13:48:00',
            'active': True
        }
    ]
