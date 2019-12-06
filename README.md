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

**HEADERS**: Authorization

**BODY**
```json
    "password": <string>
```
**RESPONSE**
 - 200: Cambio Correcto

### Usuarios

 * [Listar todos los usuarios](documentation/users.md#users): `GET /api/users`
 * [Listar un usuario](documentation/users.md#user): `GET /api/user/<id>`
 * [Crear Usuario](documentation/users.md#new-user): `POST /api/new_user`
