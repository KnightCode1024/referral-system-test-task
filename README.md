# 🔥 Реферальная система на Django + DRF 🚀

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-FF1709?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 🐳 Запуск через Docker

```bash
docker-compose up --build
```
После запуска проект будет доступен по адресу:
🌐 http://localhost:8000

## 📚 API Documentation
Документация API доступна по маршруту:
📖 http://localhost:8000/redoc

## 🛠️ API Endpoints
- 🔐 Авторизация:
  - `POST	/api/auth/send-code/`	Отправить 4-значный код на телефон 📱
  - `POST	/api/auth/verify-code/`	Подтвердить код из SMS ✅
  
- 👤 Профиль пользователя
  - `GET	/api/auth/profile/`	Получить профиль пользователя 👨‍💼
  - `PATCH	/api/auth/profile/`	Обновить инвайт-код 🆔
  
## 📊 Примеры запросов
Отправка кода авторизации: `POST /api/auth/send-code/`
```json
{
    "phone_number": "+79991234567"
}
```
Подтверждение кода: `POST /api/auth/verify-code/`
```json
{
    "phone_number": "+79991234567",
    "code": "1234"
}
```
Получение профиля: `GET /api/auth/profile/`
```
Authorization: Token <your_token>
```

## 🎁 Особенности системы
- 📱 Авторизация по SMS (с имитацией задержки 2 сек)
- 🆔 Генерация 6-значного инвайт-кода при первой авторизации
- 👥 Возможность активировать чужой инвайт-код (только 1 раз!)
- 📜 Список рефералов в профиле
- 🐳 Готовый Docker-образ для быстрого развертывания
