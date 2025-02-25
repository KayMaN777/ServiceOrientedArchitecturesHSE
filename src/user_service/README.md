# User Service
## Описание
_Сервис отвечает за авторизацию и хранение информации о пользователе. Взаимодействует с базой данных PostgreSQl, которая хранит все авторизационные данные, персональные данные и данные об активных сессиях пользователя._
![](../../doc/images/container_images/user_service.png)

### Пример запроса регистрации

```bash
> curl -X POST http://localhost:5001/register -H "Content-Type: application/json" -d '{"login": "pupa", "password": "opa", "email": "pupa@yandex.ru"}'
```

### Пример запроса авторизации

```bash
> curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d '{"login": "pupa", "password": "opa"}'
```

### Пример запроса обновления

```bash
> curl -X PUT http://localhost:5001/update -H "Content-Type: application/json" -H "Authorization: TOKEN" -d '{"firstName": "Ivan", "lastName": "Ivanovich", "birthdate": "2007-10-23", "email": "12@re.ru", "phoneNumber": "+11003234356"}'
```

### Пример запроса профиля

```bash
> curl -X GET http://localhost:5001/profile -H "Content-Type: application/json" -H "Authorization: TOKEN"
```