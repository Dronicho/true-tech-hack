## Бекенд для [True Tech Hack](https://codenrock.com/contests/true-tech-hack#/)

### Table of Contents

- [Обзор](#обзор)
- [Features](#features)
- [Установка](#усяановка)
- [Обработка видео](#обработка-видео)
- [Алгоритмы](#алгоритмы)

### Обзор

Данное приложение написано на языке Python, с использованием FastApi - фреймворк для создания API

Для обработки видео используется openCV

Для определения 18+ контента используется nsfw_mobilenet_v2 с фреймворком tensorflow

Обработанная информация хранится в mongoDB 

Информация о пользователе хранится в PostgresQL


### Features

- Python 3.10+ support
- SQLAlchemy 2.0+ support
- Асинхронность
- Миграции бд с Alembic
- Базовая авторизация с JWT
- RLAC для настройки разрешений
- Redis для кеширования
- Celery для фоновых задач
- Докеризация

### Установка

Требования:

- Python 3.11
- [Docker с Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

(Я использую pyenv для менеджмента версиями питона)

Как только все это установлено, выполните следующие шаги

1. venv:

```bash
poetry shell
```

2. Установка зависимостей:

```bash
poetry install
```

3. Запускаем бд и Редис:

```bash
docker-compose up -d
```

4. Добавить .env файл

Пример
```
# Database
POSTGRES_URL=postgresql+asyncpg://postgres:password123@127.0.0.1:5432/fastapi-db
TEST_POSTGRES_URL=postgresql://postgres:password123@127.0.0.1:5431/db-test

# Environment
ENVIRONMENT=development
DEBUG=1
SHOW_SQL_ALCHEMY_QUERIES=0

# Redis
REDIS_URL=redis://localhost:6379/7

# Celery
CELERY_BROKER_URL=amqp://rabbit:password@localhost:5672
CELERY_BACKEND_URL=redis://localhost:6379/0

```

5. Запустить миграции:

```bash
make migrate
```

6. Запустить сервер:

```bash
make run
```

Сервер будет запущен на `http://localhost:8000` и документация на `http://localhost:8000/docs`.


### Обработка видео

Чтобы обработать видео необходимо перейти в папку `process`, добавить туда видео и выполнить скрипт 
```bash
python3 process.py video // без расширения файла(.mp4)
```

После этого в монгу(`http://localhost:8081`) добавиться метадата

### Алгоритмы

(Алгоритмы основаны на [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/))

Для определения вспышек считается изменение относительной яркости между 2 кадрами
Для этого переводим кадр в LAB color space 
```python
L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
```
После этого определяем относительную яркость
```python
L = L/np.max(L)
std_dev = np.mean(L)
```
Если изменение между фреймами больше определенного значения (25%), значит это вспышка

Если вспышки происходят чаще 3 раз в секунду, то это может быть опасно
