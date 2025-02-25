## API Gateway
_Сервис, отвечающий за маршрутизацию трафика между остальными сервисами. Принимает запроса от пользователя с UI и перенаправляет в нужные сервисы._
![](../../doc/images/container_images/all_services.png)

## Примеры запросов к серверу:

### Пример запроса регистрации

```bash
> curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"login": "pupa", "password": "opa", "email": "pupa@yandex.ru"}'
```

### Пример запроса авторизации

```bash
> curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"login": "pupa", "password": "opa"}'
```

### Пример запроса обновления

```bash
> curl -X PUT http://localhost:5000/update -H "Content-Type: application/json" -H "Authorization: TOKEN" -d '{"firstName": "Ivan", "lastName": "Ivanovich", "birthdate": "2007-10-23", "email": "12@re.ru", "phoneNumber": "+11003234356"}'
```

### Пример запроса профиля

```bash
> curl -X GET http://localhost:5000/profile -H "Content-Type: application/json" -H "Authorization: TOKEN"
```