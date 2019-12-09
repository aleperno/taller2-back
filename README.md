# Foodie - Backend

[![Build Status](https://travis-ci.com/aleperno/taller2-back.svg?token=8xtxBcqxC5A8nnf9ctzM&branch=master)](https://travis-ci.com/aleperno/taller2-back)
[![Coverage Status](https://coveralls.io/repos/github/aleperno/taller2-back/badge.svg)](https://coveralls.io/github/aleperno/taller2-back)

## Introducción
Este repositorio será el código del Backend / Admin GUI para el TP de Taller de Programación 2 - FIUBA

El enunciado puede encontrarse acá [FOODIE](https://github.com/taller-de-programacion-2/taller-de-programacion-2.github.io/blob/master/trabajo-practico/enunciados/2019/2/tp/foodie.md)

## Instalación Local

 ### Requisitos
  - Python >= 3.6.X (recomendamos utilizar [virtualenv](https://medium.com/@aaditya.chhabra/virtualenv-with-virtualenvwrapper-on-ubuntu-34850ab9e765))
  - PostgreSQL (Probado en Postgres 10 y 11)

 ### Base de Datos
    
 La aplicación por defecto corre sobre una base de datos llamada `t2db` con el usuario `t2user` y contraseña `t2pass`.

 Se encuentra un script sql disponible para crear tales roles y base.
 ```
 psql < models/create_db.sql
 ```

 La aplicación también toma una variable de entorno `DATABSE_URL` en casos de querer definir un esquema diferente. El formato debe ser 
 `postgresql+psycopg2://<usuario>:<contraseña>@<host>/<database>`

 ### Python

 Para instalar el código y sus dependencias

 #### Testing / Desarrollo
 ```
 pip install -r requirements_dev.txt
 python setup.py develop
 ```

 #### Produccion
 ```
 pip install -r requirements.txt
 python setup.py develop
 ```

## Docker

  ### Requisitos
  - docker
  - docker-compose

  ### Ejecución
  El entorno de docker se contempla sólo para la ejecución del entorno productivo. No así para correr los tests.
  - docker-compose build
  - docker-compose up


### Servicios
El servidor usa diversos servicios de terceros, para poder utilizarlos se deben definir varias variables de entorno

- SENDGRID_API_KEY: Se utiliza para el servicio de emails, necesario para recuperar una cuenta
- GOOGLE_API_KEY: Necesaria para los servicios de maps.
- FIREBASE_AUTH: Necesaria para el envio de notificaciones y mensajes a los usuarios.

En `docker-compose.yml` posee las variables declaradas, pero el valor debe ser reemplazado por los correspondientes

---

## Tests  

Habiendo instalado el entorno como testing, para correr las pruebas localmente
```make test```

---

## Ejecucion

Para ejecutarlo localmente existe una entrada de `Makefile`

```make run```

o en su defecto

```gunicorn app:app```

Esto localmente iniciará un servidor escuchando en 

`http://localhost:8000`

---
## Logging

Se puede modificar el nivel de logging de la aplicación mediante una variable de entorno `LOGLEVEL`, por ejemplo (case-sensitive)
 - LOGLEVEL=INFO
 - LOGLEVEL=DEBUG
 - LOGLEVEL=WARNING
 - LOGLEVEL=ERROR

---
## Datos de Prueba

Si se corre la aplicación por primera vez, existe la forma de cargar datos de prueba.

Con la aplicación corriendo:
    ```
    python scripts/load_dummy_data.py [-t target]
    ```
donde `target` es opcional y es la ubicación de la aplicación, si no se especifíca apunta a `localhost:8000`

---
# Arquitectura

## Deploy

Actualmente la aplicación se encuentra con un esquema de `continous-delivery`. Cada vez que se pushea a `master` ocurre el siguiente flujo.

    Tests => Coverage => Heroku

Todos los tests reportan el cóverage a [coveralls](https://coveralls.io/github/aleperno/taller2-back).
Si el test es exitoso, se *triggerea* un build de Heroku.

Todo este proceso es automático, lo que nos permite fácilmente
 - Identificar Pull Requests que no cumplan los requisitos para mergearse (tests fallidos / coverage)
 - Identificar fallas rápidamente
 - Poder tener la nueva versión corriendo sin intervención


## Estructura Interna

La estructura de la aplicación es relativamente sencilla y detallaremos los elementos principales.

 - **Modelos**: Estos definen cómo se guarda la información en la base de datos. Utilizamos un ORM, que nos permite interactuar con la base mediante objetos.


 - **Recursos**: Estos representan los recursos (endpoints) que brinda la aplicación.

### Modelo
El modelo general cuenta con pocas entidades
 - **Usuario**: Representa a un usuario, ya sea del tipo común o delivery.
 - **Shop**: Representa un comercio
 - **Producto**: Representa los productos que poseen los shops.
 - **Ordenes**: Representan los pedidos que realizan los usuarios.

 Un usuario se relaciona con otro usuario **SÓLO** a través de una orden.

Existen entidades adicionales que son auxiliares al modelo de negocio / estructura. Ejemplo

 - **Tokens**: Representan los tokens de autorización
 - **Reviews**: Representan los reviews hechos por una orden
 - **Delivery Location**: Representa el estado (ubicación) de un delivery


---

# API

[http://taller2-back.herokuapp.com/api](http://taller2-back.herokuapp.com/api)

Todos los endpoints poseen el prefijo `/api/`

## Schemas
Todos los endpoints que soporten el verbo **PUT** y **POST** poseen validadores de esquema, es decir validan que el *body* enviado cumpla con una serie de parámetros.

En caso de que el schema no se cumpla, el servidor como *status_code* devolverá `400 BAD REQUEST` y en el cuerpo de la respuesta enviará un detalle del error.

Ejemplos:

 - Falta un parámetro
    ```json
    {
        "password": [
            "Missing data for required field."
        ]
    }
    ```
- Tipo incorrecto
    ```json
    {
        "password": [
            "Not a valid string"
        ]
    }
    ```

En este sentido decimos que en cierto modo la API está auto documentada, con levantar el servidor y hacer requests vacios, el mismo nos responderá que nos falta enviar.

## Convenciones en la respuesta
Se sigue la siguiente convención de códigos de estado

- **200**: Obtencion o modificacion exitosa de un recurso.
- **201**: Creacion de un objeto exitoso.
- **400**: En caso de un request malformado, ya se por esquema o porque no cumple con los requerimientos del modelo.
- **404**: Recurso no encontrado

## Admins
Por defecto el sistema posee un usuario administrador, cuyo email es `admin@foodie.com` y contraseña `admin123`

### Login
**URL**: `/api/admin/login`

**METHODS** POST

**BODY**
```json
    "email": <string>,
    "password": <string>,
```
**RESPONSE**
 - 404: Usuario no existe
 - 403: Contraseña incorrecta
 - 200: Login correcto. Se devuelve `{'Authorization': <token>}`

---

### Change Password
**URL**: `/api/admin/change_password`

**METHODS**: PUT

**BODY**
```json
    "password": <string> # min 6 chars
```

**RESPONSE**
 - 200: Cambio Correcto

---

### Nuevo Admin
**URL**: `/api/admin/new_admin`

**METHODS**: POST

**BODY**
```json
    "name": <string>,
    "surname": <string>,
    "email": <email>,
    "password": <string> # min 6 chars
```

**RESPONSE**
 - 201: Usuario creado correctamente

---

### Obtener y Editar Usuarios

**URL**: `/api/admin/users/<user_id>`

**METHODS**: GET, PUT, DELETE

- **GET**: Si se especifica el `user_id` devuelve los datos de dicho usuario. Si se omite, se devuelve una lista con los datos de todos los usuarios. Ejemplo de los datos de un usuario:
    ```json
    {
        "active": true,
        "cash_balance": 0.0,
        "creation_date": "2019-12-01T14:35:54",
        "email": "hola@gmail.com",
        "favor_balance": 0.0,
        "id": 1,
        "name": "Elaine",
        "password": "insecure",
        "phone": "4444-5555",
        "photo_url": null,
        "reputation": 5.0,
        "role": "user",
        "status": "active",
        "subscription": "premium",
        "surname": "Simoneaux"
    }
    ```
    Respuestas:
     - 200: Ok
     - 404: `user_id` no existe
- **PUT**: Permite modificar los datos de un usuario, es necesario especificar el `user_id`.
    Todos los campos son editables, excepto `reputation`, `id` y `creation_date`

    Asímismo se debe respetar las restricciones del modelo.
    - Role: Si a un usuario se le cambia el rol al de delivery y el mismo no poseeia foto, el sistema no te deja cambiarle sólo el rol sin especificar una imagen.
    - Role: Sólo se permite `user` o `delivery`
    - Subscription: Sólo se permite `flat` o `premium`
    - Email: No se permiten emails duplicados.

- **DELETE**: Setea un usuario como `active=False`

---

### Crear, obtener y editar Comercios

**URL**: `/api/admins/shops/<shop_id>`

**METHODS**: POST, PUT, GET, DELETE

- **GET**: Obtiene la informacion de los comercios. Si no se especifica el `shop_id` devuelve todos los shops.
Ejemplo
```json
{
    "id": 1,
    "name": "Pizzeria los HDP",
    "description": "La peor pizzeria de la ciudad",
    "address": "Cabildo 505",
    "location": "-34.571691,-58.4441975",
    "category": "pizzeria",
    "creation_date": "2019-12-01T14:35:58",
    "active": true
}
```

- **POST**: Crea un nuevo comercio
```json
{
	"name": "Pizzeria los HDP",
	"description": "La peor pizzeria de la ciudad",
	"address": "Cabildo 500",
	"location": "-34.571691,-58.4441975",
	"category": "pizzeria"
}
```

- **PUT**: Se modifica un comercio, admite los mismos campos que el **POST** + `active=True` para re-habilitar un comercio.
- **DELETE**: Se setea `active=False` para un comercio.

---

### Crear, Obtener y Editar Productos

**URL**: `/api/admin/products/`
**METHODS**: POST, GET, PUT, DELETE

 - **GET**: Devuelve todos los productos en la plataforma
 ```json
 [
     {
        "id": 1,
        "shop_id": 1,
        "name": "Pizza de Anana",
        "description": "Salsa de Tomate, Mozzarella y rodajas de anana",
        "category": "pizzas",
        "price": 300.0,
        "creation_date": "2019-12-01T14:36:01",
        "active": true
    }...
 ]
 ```
 - **POST**: Crea un nuevo producto
 ```json
    {
    'shop_id': <shop_id>,  # Debe existir
    'name': 'Sanguche Milanesa',
    'description': 'Sanguche de Milanesa',
    'category': 'sanguche',
    'price': 200,
    }
 ```

 - **PUT**: Se edita un producto, se admiten los siguientes campos
 ```json
    "id": <id del producto a editar> # Obligatorio,
    "shop_id": <el id de otro shop>,
    "name": <string>,
    "description": <string>,
    "category": <string>,
    "price": <float>,
    "active": <boolean>
 ```
 - **DELETE**: Se setea `active=False` para dicho producto

---

### Ver Órdenes existentes

**URL**: `/api/admin/orders`
**METHODS**: GET

Obtiene la informacion de todas las órdenes en el sistema. Ejemplo:

```json
[
    {
        "id": 3,
        "shop_id": 2,
        "user_id": 7,
        "delivery_id": null,
        "user_location": "-34.572259,-58.4843497",
        "shop_location": "-34.5627322,-58.4564323",
        "distance": 4130,
        "status": "pending",
        "status_id": 0,
        "favor": false,
        "products": [
            {
                "id": 3,
                "quantity": 1
            }
        ],
        "price": 230.0,
        "product_prices": 2.99,
        "creation_date": "2019-12-08T04:13:56",
        "order_metadata": {
            "creation_date": "2019-12-08T04:13:56"
        },
        "delivery_revenue": null,
        "address": "Paseo Colón 850"
    },...
]
```

---

### Ver y Editar reglas de precios

**URL**: `/api/admin/pricing
**METHODS**: GET, PUT

 - **GET**: Obtiene las reglas actuales de precios
 ```json
 {
    "flat_min_km": 2,
    "flat_base": 200,
    "flat_extra_km": 15,
    "premium_min_km": 3,
    "premium_base": 20,
    "premium_extra_km": 12,
    "delivery_revenue_perc": 85
}
```

- **PUT**: Se editan las reglas. No se puede omitir ningun campo, se debe enviar todo el JSON.

---

## Usuarios

A continuacion se detallaran los endpoints para los usuarios

## Registro / Autenticación

### Nuevo Usuario

**URL**: `/api/user`
**METHODS**: POST
Ejemplo:

```json
    {
        'name': name,
        'surname': surname,
        'email': email,
        'password': 'insecure', # min 6 chars
        'phone': '4444-5555',
        'role': 'user' or 'delivery' # opcional, defaults to user,
        'subscription': 'flat' or 'premium' # optional, defaults to flat,
        'photo_ur': # Si el usuario es delivery, debe especificar una imagen.
    }
```

---

### Login
**URL**: `/api/login`
**METHODS**: POST
```json
{
    "email": ,
    "password:,
}
```
Devuelve `{'Authorization': <token>}`

---

### Facebook Login
**URL**: `/api/fb_login`
**METHODS**: POST
```json
{
    "fb_access_token": <token>
}
```
Devuelve `{'Authorization': <token>}`

---

### Contraseña Olvidada
**URL**: `/api/forgot_password`
**METHODS**: POST
```json
    "email":,
```
Se le envia a dicho mail un token para recuperar su contraseñá

---

### Recuperar Contraseña
**URL**: `/api/reset_password`
**METHODS**: POST
```json
    "email": ,
    "password": ,
    "confirm_password": ,
    "token": ,
```

El servidor valida que el token sea válido (no expirado) y no haya sido usado con anterioridad. Asímismo valida que ambos campos de la contraseña cumplan los requerimientos (6 caracteres) y coincidan entre sí.

---

### Informacion del usuario
**URL**: `/api/user`
**METHODS**: GET
**HEADERS**: Authorization

Devuelve la información del usuario como diccionario. Se requiere que esté seteado el header de `Authorization` con el token obtenido en el login.

```json
{
    "id": 9,
    "name": "Alejandro",
    "surname": "Pernin",
    "email": "ale.pernin@gmail.com",
    "password": "insecure",
    "creation_date": "2019-11-02T20:39:57",
    "status": "active",
    "phone": "222222222",
    "role": "delivery",
    "subscription": "flat",
    "photo_url": "http://asd.com",
    "active": true,
    "cash_balance": 0.0,
    "favor_balance": 0.0,
    "reputation": null
}
```
---

## Flujo de pedido

### Ver Comercios

Devuelve todos los comercios activos y que posean productos

**URL**: `/api/shops`
**METHODS**: GET

```json
[
    {
        "id": 2,
        "name": "Confiteria Murano",
        "description": "Tes y masitas para morirse",
        "address": "Belgrano",
        "location": "-34.5627322,-58.4564323",
        "category": "facturas",
        "creation_date": "2019-12-01T14:35:59",
        "active": true
    },...
]
```

### Ver productos comercio

Devuelve los productos activos de un comercio

**URL**: `/api/shops/<shop_id>/products
**METHODS**: GET
```json
[
    {
        "id": 3,
        "shop_id": 2,
        "name": "Te Negro",
        "description": "Te negro, como el alma de la misma murano",
        "category": "infusiones",
        "price": 2.99,
        "creation_date": "2019-12-01T14:36:03",
        "active": true
    },
    {
        "id": 4,
        "shop_id": 2,
        "name": "Masitas Finas",
        "description": "Masitas Finas con un ingrediente secreto, hecho por la mismisima yiya.",
        "category": "dulces",
        "price": 5.0,
        "creation_date": "2019-12-01T14:36:03",
        "active": true
    }
]
```

### Efectuar Orden

**URL**: `/api/orders`
**METHODS**: POST
```json
{
	"user_id": 1,
	"shop_id": 1,
	"user_location": "-34.572259,-58.4843497",
	"products": [
        {"id": 1, "quantity": 1}, ...
        ],
	"favor": false
}
```

El servidor responde con

```json
{
    "order_id": # El id de la orden
    "available": [
        # Un listado de deliveries disponibles, de haber
    ],
    "closest": , # El ID del delivery mas cercano, de haber
    "delivery_price":, # El costo del delivery
    "order_price": # El costo de los productos
} 
```

ejemplo

```json
{
    "order_id": 477,
    "available": [
        {
            "user_id": 9,
            "location": "-34.5604742,-58.4606362",
            "available": true,
            "last_updated": "2019-12-07T02:53:41",
            "name": "Alejandro",
            "surname": "Pernin",
            "reputation": null,
            "photo_url": "http://asd.com",
            "distance": 2621
        },
        {
            "user_id": 11,
            "location": "-34.6122683,-58.3917467",
            "available": true,
            "last_updated": "2019-12-07T02:36:33",
            "name": "Bart",
            "surname": "Simpson",
            "reputation": null,
            "photo_url": "http://asd.com",
            "distance": 7946
        },
        {
            "user_id": 13,
            "location": "-34.7643059,-58.2025602",
            "available": true,
            "last_updated": "2019-12-07T03:08:04",
            "name": "Lisa",
            "surname": "Simpson",
            "reputation": null,
            "photo_url": "http://asd.com",
            "distance": 40602
        }
    ],
    "closest": 9,
    "delivery_price": 56,
    "order_price": 300.0
}
```

---

### Elegir Delivery

El usuario debe elegir el delivery para la orden

**URL**: `/api/orders/choose_delivery`
**METHODS**: POST

```json
    "user_id": # El id del él,
    "order_id": # El id de la orden,
    "delivery_id": #El id del delivery seleccionado
```

**Repuestas**: Hay dos opciones
 - El delivery que se quiso seleccionar ya no se encuentra disponible
 ```json
    "status": "Choose another",
    "status_id": 0,
 ```
 - El delivery seleccionado está disponible y está pendiente que acepte el pedido
 ```json
    "status": "Waiting delivery acceptance",
    "status_id": 1,
 ```

 En ambos casos se devuelve `200` como status code.

---

### Consultar estado de la orden

**URL**: `/api/orders/<order_id>/status`
**METHODS**: GET,

La respuesta varía acorde el estado de la orden
- La orden no posee delivery elegido
```json
{
    "order_id": 477,
    "available": [
       ...
    ],
    "closest": 9,
    "delivery_price": 56,
    "order_price": 300.0,
    "status_id": 0,
    "status": "pending",
}
```
- La orden posee un delivery elegido, el cuál todavía no confirmó
```json
{
    "order_id": 477,
    "available": [
       ...
    ],
    "closest": 9,
    "chosen": 9,
    "delivery_price": 56,
    "order_price": 300.0,
    "status_id": 1,
    "status": "pending_delivery_acceptance",
}
```
- La orden fue aceptada por el delivery. Se devuelve la ubicacion y datos del delivery
```json
{
    "status": "accepted",
    "status_id": 2,
    "delivery_location": "-34.6122683,-58.3917467",
    "delivery_data": {
        "name": "Bart",
        "surname": "Simpson",
        "reputation": null,
        "photo_url": "http://asd.com"
    }
}
```
- El delivery se encuentra en el local, esperando el pedido
```json
{
    "status": "in_shop",
    "status_id": 3,
    "delivery_location": "-34.6122683,-58.3917467",
    "delivery_data": {
        "name": "Bart",
        "surname": "Simpson",
        "reputation": null,
        "photo_url": "http://asd.com"
    }
}
```

- El delivery salió del local y va rumbo al domicilio
```json
{
    "status": "out_shop",
    "status_id": 4,
    "delivery_location": "-34.6122683,-58.3917467",
    "delivery_data": {
        "name": "Bart",
        "surname": "Simpson",
        "reputation": null,
        "photo_url": "http://asd.com"
    }
}
```
- El delivery marcó que ya entregó la orden
```json
{
    "status": "delivered",
    "status_id": 5,
    "delivery_location": "-34.6122683,-58.3917467",
    "delivery_data": {
        "name": "Bart",
        "surname": "Simpson",
        "reputation": null,
        "photo_url": "http://asd.com"
    }
}
```
- Se confirmó la recepcion de la orden
```json
{
    "status": "confirmed",
    "status_id": 6,
    "delivery_location": "-34.6122683,-58.3917467",
    "delivery_data": {
        "name": "Bart",
        "surname": "Simpson",
        "reputation": null,
        "photo_url": "http://asd.com"
    }
}
```
- La orden fue cancelada
```json
    "status": "cancelled",
    "status_id": 9,
```

---

 ### Cancelar Orden
 La orden sólo se puede cancelar si todavía no se elegió delivery o el mismo todavía no confirmó el pedido. Una vez que el delivery acepta una orden, esta no se puede cancelar.

 **URL**: `/api/orders/<order_id>/cancel`
 **METHODS** POST
 ```json
    "user_id": # El id del usuario
 ```

 Si la orden se logró cancelar, el servidor devuelve

 ```json
    "status": "cancelled",
    "status_id": 9
 ```

 caso contrario devuelve el estado actual de la orden.

 ---

 ### Confirmar Recepción Orden

 **URL**: `/api/orders/confirm`
 **METHODS**: POST
 ```json
    "user_id":,
    "order_id":, 
```

---

### Calificar Pedido

Este endpoint le permite a ambas partes calificar a su contraparte

**URL**: `/api/orders/review`
**METHODS**: POST
```json
    "user_id": ,
    "order_id": ,
    "review": <float>
```

---

### Ponerse como Disponible / Actualizar ubicacion

Este endpoint sirve para que los usuarios se marquen como disponibles para realizar envios y/o actualizar su estado durante un envio.

**URL**: `/api/deliveries/status`
**METHODS**: GET, POST

 - **GET**: Devuelve el status de todos los deliveries. Esto en realidad debería ser parte de `/api/admins`
 ```json
 [
     {
        "user_id": 6,
        "location": "-34.5752085,-58.40428670000001",
        "available": false,
        "last_updated": "2019-12-01T14:36:08"
    },...
 ]
 ```

 - **POST**: Un usuario actualiza su estado
```json
{
    "user_id": ,# El id del usuario
    "location":, # Las coordenadas
    "available": <boolean> # Si se encuentra apto para recibir un pedido (true) u ocupado (false).
}
```

---

### Obtener ordenes disponibles / actualizar estado

Este endpoint sirve para quien va a realizar un delivery, vea que ordenes tiene disponibles para aceptar. Y una vez aceptada, actualizra el estado

**URL**: `/api/orders/available/<user_id>`
**METHODS**: GET, PUT

 - **GET**: Obtiene todas las ordenes pendientes para aceptar. Figura la ubicacion del comercio, del usuario, la distancia entre ambos; la distancia entre el delivery (segun la ultima reportada) y el comercio, y la distancia total.
 Asímismo figuran los datos publicos del usuario y cuál será la ganancia del delivery.
 ```json
 [
     {
        "id": 4,
        "shop_id": 4,
        "user_id": 1,
        "user_location": "-34.572259,-58.4843497",
        "shop_location": "-34.571691,-58.4441975",
        "distance": 5151,
        "favor": false,
        "products": [
            {
                "id": 1,
                "quantity": 1
            }
        ],
        "address": null,
        "distance_to_shop": 190920,
        "total_distance": 196071,
        "user_data": {
            "name": "Elaine",
            "surname": "Simoneaux",
            "reputation": 5.0
        },
        "revenue": 55.25
    },...
 ]
 ```

 - **PUT**: Con esto aceptará y actualizará los estados de las ordenes
    ```json
        "order_id": # Id de la orden,
        "status": 
    ```
    Donde el status puede ser `accepted`, `in_shop`, `out_shop` o `delivered`.