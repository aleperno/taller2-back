import requests
import json
from urllib.parse import urljoin
import argparse


URL = 'http://localhost:8000'
HEADERS = {"Accept":"*/*",
           "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
           "Content-Type":"application/json; charset=utf-8",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default=URL, help='Server URL')
    return parser.parse_args()


def new_users(base_url):
    url = urljoin(base_url, 'api/new_user')
    r = requests.post(url, json={
        'name': 'Juancito',
        'surname': 'Lopez',
        'email': 'juancito@gmail.com',
        'password': 'insecure',
        'phone': '4781-6140'
    })
    requests.post(url, json={
        'name': 'Benicio',
        'surname': 'Juarez',
        'email': 'bjuarez@gmail.com',
        'password': '123456789',
        'phone': '555-6666'
    })


def new_shops(base_url):
    url = urljoin(base_url, 'api/admin/shops')
    los_hdp = {
        'name': 'Pizzeria los HDP',
        'description': 'La peor pizzeria de la ciudad',
        'address': 'Cabildo 500',
        'location': '4444,5555',
        'category': 'pizzeria'
    }
    murano = {
        'name': 'Confiteria Murano',
        'description': 'Tes y masitas para morirse',
        'address': 'Monserrat',
        'location': '4444,5555',
        'category': 'facturas'
    }
    r = requests.post(url, json=los_hdp)
    requests.post(url, json=murano)


def new_products(base_url):
    url = urljoin(base_url, '/api/admin/products')
    pizza = {
        'shop_id': 1,
        'name': 'Pizza de Anana',
        'description': 'Salsa de Tomate, Mozzarella y rodajas de anana',
        'category': 'pizzas',
        'price': 11.99,
    }
    te = {
        'shop_id': 2,
        'name': 'Te Negro',
        'description': 'Te negro, como el alma de la misma murano',
        'category': 'infusiones',
        'price': 2.99,
    }
    masitas = {
        'shop_id': 2,
        'name': 'Masitas Finas',
        'description': 'Masitas Finas con un ingrediente secreto, hecho por la mismisima yiya.',
        'category': 'dulces',
        'price': 5,
    }
    prods = [pizza, te, masitas]
    for p in prods:
        requests.post(url, json=p)

def main():
    args = parse_args()
    base_url = args.target
    new_users(base_url)
    new_shops(base_url)
    new_products(base_url)


if __name__ == '__main__':
    main()
