# Users Endpoint

## Users

Lista todos los usuarios en la base

**URL**: `/api/users`

**Method**: `GET`

**Autenticacion**: NO

**Autorizacion**: NO

---

## User

Lista la información de un usuario dado

**URL**: `/api/user/<id>`

**Method**: `GET`

**Autenticacion**: NO

**Autorizacion**: NO

### Errores

#### ID inexistente

**Condicion**: No hay usuario con dicho `id`

**Status Code**: `404 NOT FOUND`

---

## New User

**URL**: `/api/new_user`

**Method**: `POST`

**Autenticacion**: NO

**Autorizacion**: NO

**Body (JSON)**:
```json
{
    "name": "John",
    "surname": "Richards",
    "email": "some_email@gmail.com",
    "password": "really_secure_password"
}
```

### Exitoso

**Status Code**: `201 CREATED`

**Content**:
```json
{
    "id": 22,
    "name": "John",
    "surname": "Richards",
    "email": "some_email@gmail.com",
    "password": "really_secure_password"
}
```

### Errores

#### Email ya registrado

**Status Code**: `400 BAD REQUEST`

**Content**: `Email already registered`

#### Email inválido

**Status Code**: `400 BAD REQUEST`

**Content**:
```json
{
    "email": [
        "Not a valid email address."
    ]
}
```

#### Campo faltante

**Status Code**: `400 BAD REQUEST`

**Content**:
```json
{
    "password": [
        "Missing data for required field."
    ]
}
```

#### Campo Valor inválido

**Status Code**: `400 BAD REQUEST`

**Content**:
```json
{
    "name": [
        "Not a valid string."
    ]
}
```
