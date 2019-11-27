import requests
import json
import names
import random
from urllib.parse import urljoin
import argparse


URL = 'http://localhost:8000'
HEADERS = {"Accept":"*/*",
           "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
           "Content-Type":"application/json; charset=utf-8",
}

CANT_USUARIOS = 3
USUARIOS = []

CANT_DELIVERIES = 3
DELIVERIES = []

SHOPS = {}

COORDS = [
    '-34.5704073,-58.4443573',
    '-34.5736922,-58.459543',
    '-34.5607083,-58.4580788',
    '-34.5681196,-58.4373488',
    '-34.580486,-58.4507462',
    '-34.553556,-58.452136',
    '-34.5579187,-58.45998609999999',
    '-34.5471301,-58.45730039999999',
    '-34.5745347,-58.4258525',
    '-34.5996931,-58.4392779',
    '-34.580926,-58.42230499999999',
    '-34.5746879,-58.4863292',
    '-34.60282,-58.46571499999999',
    '-34.5752085,-58.40428670000001',
    '-34.5879527,-58.41012070000001',
    '-34.5457365,-58.48834050000001',
    '-34.5891469,-58.39816699999999',
    '-34.5853977,-58.41599609999999',
    '-34.589417,-58.393466',
    '-34.5727666,-58.5077894'
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default=URL, help='Server URL')
    return parser.parse_args()


def _random_user():
    name, surname = names.get_full_name().split(' ')
    email = f"{name}_{surname}@gmail.com".lower()

    data = {
        'name': name,
        'surname': surname,
        'email': email,
        'password': 'insecure',
        'phone': '4444-5555'
    }
    return data


def new_users(base_url):
    url = urljoin(base_url, 'api/new_user')
    for i in range(CANT_USUARIOS):
        data = _random_user()
        r = requests.post(url, json=data)
        assert r.status_code == 201
        _id = r.json().get('id')
        DELIVERIES.append(r.json())

    for i in range(CANT_DELIVERIES):
        data = _random_user()
        data.update({
            'role': 'delivery',
            'photo_url': 'http://asd.com'
        })
        r = requests.post(url, json=data)
        assert r.status_code == 201
        _id = r.json().get('id')
        USUARIOS.append(r.json())


def new_shops(base_url):
    url = urljoin(base_url, 'api/admin/shops')
    los_hdp = {
        'name': 'Pizzeria los HDP',
        'description': 'La peor pizzeria de la ciudad',
        'address': 'Cabildo 500',
        'location': '-34.571691,-58.4441975',
        'category': 'pizzeria'
    }
    murano = {
        'name': 'Confiteria Murano',
        'description': 'Tes y masitas para morirse',
        'address': 'Belgrano',
        'location': '-34.5627322,-58.4564323',
        'category': 'facturas'
    }
    garcia = {
        'name': 'Garcia Castro',
        'description': 'Comida Gourmet',
        'address': 'Dorrego 1311',
        'location': '-34.5865603,-58.4474571',
        'category': 'comida'
    }
    buen_libro = {
        'name': 'El Buen Libro',
        'description': 'Sanguches y Comidas',
        'address': 'Reconquista 631',
        'location': '-34.600452,-58.372497',
        'category': 'sanguches, comidas'
    }

    shops = [
        los_hdp,
        murano,
        garcia,
        buen_libro
    ]
    for shop in shops:
        r = requests.post(url, json=shop)
        assert r.status_code == 201
        _json = r.json()
        _id = _json.get('id')
        SHOPS[shop.get('name')] = _id


def new_products(base_url):
    url = urljoin(base_url, '/api/admin/products')

    # Productos de Pizzeríá
    pizza_shop_id = SHOPS.get('Pizzeria los HDP')

    pizza_anana = {
        'shop_id': pizza_shop_id,
        'name': 'Pizza de Anana',
        'description': 'Salsa de Tomate, Mozzarella y rodajas de anana',
        'category': 'pizzas',
        'price': 300,
    }

    pizza_jamon = {
        'shop_id': pizza_shop_id,
        'name': 'Pizza Jamon y Morrones',
        'description': 'Salsa de Tomate, Mozzarella, Jamón y Morrones',
        'category': 'pizzas',
        'price': 400,
    }

    # Productos de Panaderia
    murano_id = SHOPS.get('Confiteria Murano')
    te = {
        'shop_id': murano_id,
        'name': 'Te Negro',
        'description': 'Te negro, como el alma de la misma murano',
        'category': 'infusiones',
        'price': 2.99,
    }
    masitas = {
        'shop_id': murano_id,
        'name': 'Masitas Finas',
        'description': 'Masitas Finas con un ingrediente secreto, hecho por la mismisima yiya.',
        'category': 'dulces',
        'price': 5,
    }

    # Productos de Garcia
    garcia_id = SHOPS.get('Garcia Castro')
    kobe = {
        'shop_id': garcia_id,
        'name': 'Kobe Burger',
        'description': 'Hamburguesa de carne Kobe, con panceta y queso provolone. Acompañado con papas rústicas',
        'category': 'hamburguesas',
        'price': 320,
    }
    cesar = {
        'shop_id': garcia_id,
        'name': 'Cesar Salad',
        'description': 'Ensalada de hojas verdes, pollo, salsa cesar, queso parmesao y croutones',
        'category': 'ensaladas',
        'price': 280,
    }

    # Productos del buen libro
    libro_id = SHOPS.get('El Buen Libro')

    crudo = {
        'shop_id': libro_id,
        'name': 'Sanguche Jamon Crudo y Rucula',
        'description': 'Sanguche de Jamón Crudo, Queso tybo y rúcula en pan francés con manteca',
        'category': 'sanguche',
        'price': 230,
    }

    milanesa = {
        'shop_id': libro_id,
        'name': 'Sanguche Milanesa',
        'description': 'Sanguche de Milanesa',
        'category': 'sanguche',
        'price': 200,
    }

    prods = [pizza_anana, pizza_jamon, te, masitas, kobe, cesar, crudo, milanesa]
    for p in prods:
        r = requests.post(url, json=p)
        assert r.status_code == 201


def deliveries_locations(base_url):
    url = urljoin(base_url, '/api/deliveries/status')
    for delivery in DELIVERIES:
        data = {
            'user_id': delivery['id'],
            'available': True,
            'location': random.choice(COORDS)
        }
        r = requests.post(url, json=data)
        assert r.status_code in (200, 201)


def main():
    args = parse_args()
    base_url = args.target
    new_users(base_url)
    new_shops(base_url)
    new_products(base_url)
    deliveries_locations(base_url)


if __name__ == '__main__':
    main()