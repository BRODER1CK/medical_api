# API Server

## **Структура репозитория**

1. **tests:** `patients/tests.py`
2. **code:** `patients/` (основная директория с кодом проекта)
3. **docker:** `docker-compose.yaml`
4. **migrations:** `patients/migrations/`

---

## **Инструкции по локальному запуску**

### **1. Клонирование репозитория**

```bash
git clone <URL_репозитория>
cd <Название_директории>
```

### **2. Настройка переменных окружения**

Создайте файл `.env` в корневой директории проекта и укажите следующие параметры:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_NAME=your_db_name
```

### **3. Запуск через Docker**

1. Убедитесь, что установлены Docker и Docker Compose.
2. Запустите команду:

```bash
docker-compose up --build -d
```

Проект будет доступен на `http://localhost:8000/`.

---

## **Примеры запросов**

### **1. Получение JWT-токена**

**URL:** `/api/login/`  
**Метод:** POST  
**Тело запроса:**

```json
{
    "username": "<USERNAME>",
    "password": "<PASSWORD>"
}
```

**Пример ответа:**

```json
{
    "refresh": "<REFRESH_TOKEN>",
    "access": "<ACCESS_TOKEN>"
}
```

### **2. Получение списка пациентов**

**URL:** `/api/patients/`  
**Метод:** GET  
**Заголовок:**

```
Authorization: Bearer <ACCESS_TOKEN>
```

**Пример ответа:**

```json
[
    {
        "id": 1,
        "date_of_birth": "1990-01-01",
        "diagnoses": ["diagnosis1", "diagnosis2"],
        "created_at": "2025-01-01T12:00:00Z"
    }
]
```

---

## **Покрытие тестами**

- Покрытие тестами: **80%+**
- Используемый инструмент: **`unittest` и `rest_framework.test`**
- Команда для запуска тестов:

```bash
docker-compose exec web poetry run python manage.py test
```

---

## **Зависимости**

- **Django**: для основного API.
- **Django REST Framework**: для работы с API.
- **SimpleJWT**: для аутентификации.
- **Poetry**: для управления зависимостями.

---

## **Для разработчиков**

1. **Создание суперпользователя:**

После запуска контейнеров выполните:

```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

2. **Миграции:**

```bash
docker-compose exec web poetry run python manage.py makemigrations
```
```bash
docker-compose exec web poetry run python manage.py migrate
```

