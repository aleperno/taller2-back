# Foodie - Backend

[![Build Status](https://travis-ci.com/aleperno/taller2-back.svg?token=8xtxBcqxC5A8nnf9ctzM&branch=master)](https://travis-ci.com/aleperno/taller2-back)
[![Coverage Status](https://coveralls.io/repos/github/aleperno/taller2-back/badge.svg)](https://coveralls.io/github/aleperno/taller2-back)

## Introducción
Este repositorio será el código del Backend / Admin GUI para el TP de Taller de Programación 2 - FIUBA

El enunciado puede encontrarse acá [FOODIE](https://github.com/taller-de-programacion-2/taller-de-programacion-2.github.io/blob/master/trabajo-practico/enunciados/2019/2/tp/foodie.md)

## Instalación

 ### Requisitos
  - Python 3.6.X (recomendamos utilizar [virtualenv](https://medium.com/@aaditya.chhabra/virtualenv-with-virtualenvwrapper-on-ubuntu-34850ab9e765))
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

## API

[http://taller2-back.herokuapp.com/api](http://taller2-back.herokuapp.com/api)

Todos los endpoints poseen el prefijo `/api/`

### Usuarios

 * [Listar todos los usuarios](documentation/users.md#users): `GET /api/users`
 * [Listar un usuario](documentation/users.md#user): `GET /api/user/<id>`
 * [Crear Usuario](documentation/users.md#new-user): `POST /api/new_user`
