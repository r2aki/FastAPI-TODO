***

# FastAPI TODO API

Простой, но “production‑образный” TODO/Task‑менеджер на FastAPI с аутентификацией по JWT, асинхронным SQLAlchemy 2.0, Alembic и Docker. Поддерживает пользователей, проекты и задачи, фильтрацию, пагинацию и интеграционные тесты на pytest.[1]

## Стек технологий

- FastAPI (async Web API). 
- Pydantic v2 (валидация и схемы). 
- Async SQLAlchemy 2.0 + PostgreSQL (основная БД).[2]
- Alembic (миграции). 
- PyJWT (JWT‑токены). 
- passlib[bcrypt] (хэширование паролей). 
- Docker + docker compose (контейнеризация).[3]
- pytest (интеграционные тесты API).[4][1]
- aiosqlite (тестовая БД SQLite для тестов).[5][6]

## Возможности

- Регистрация пользователей с безопасным хранением паролей (bcrypt). 
- Логин и выдача JWT‑токена (`/auth/login`). 
- Защищённые эндпоинты через `OAuth2PasswordBearer` и `get_current_user`. 
- Проекты:
  - создание, получение по id, список с пагинацией, удаление;  
  - каждый проект привязан к владельцу, чужие проекты недоступны. 
- Задачи:
  - создание с привязкой к проекту и исполнителю;  
  - фильтрация по проекту, статусу и приоритету;  
  - обновление и удаление только своих задач. 
- Интеграционные тесты:
  - регистрация и логин;
  - работа защищённых эндпоинтов (`/projects`, `/tasks`) через тестовую БД и `TestClient`.[7][1]

## Запуск через Docker

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd <папка-проекта>
```

### 2. Настроить переменные окружения

Создай `.env` (или используй существующий) с ключевыми настройками:

```env
DATABASE_URL=postgresql+asyncpg://taskuser:taskpass@db:5432/taskdb
SECRET_KEY=случайная_строка_32+_символа
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

`SECRET_KEY` можно сгенерировать, например, `openssl rand -hex 32`. 

### 3. Собрать и запустить

```bash
docker compose up --build
```

- Backend поднимется на `http://localhost:8000`.[3]
- Swagger‑документация доступна по адресу `http://localhost:8000/docs`. 

### 4. Применить миграции (если не автоматизировано в entrypoint)

В отдельном терминале:

```bash
docker compose exec app alembic upgrade head
```

После этого БД готова к работе. 

## Основные эндпоинты

Базовый URL: `http://localhost:8000`.

### Аутентификация

- `POST /users/` — регистрация пользователя (username, email, password).  
- `POST /auth/login` — логин, в ответе `access_token` и `token_type="bearer"`. 

Пример логина:

```http
POST /auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "Test1234"
}
```

Ответ:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Полученный токен нужно передавать в заголовке:

```http
Authorization: Bearer <jwt>
```

### Пользователи

- `GET /users/` — список пользователей (может быть защищён).  
- `GET /users/me` — данные текущего пользователя (через JWT). 

### Проекты

Все маршруты требуют авторизации (JWT).

- `GET /projects` — список проектов текущего пользователя. Поддерживает:  
  - `limit`, `offset` — пагинация. 
- `POST /projects` — создать проект:
  - тело: `{ "name": "...", "description": "..." }`
  - `owner_id` берётся из текущего пользователя.
- `GET /projects/{project_id}` — детальная информация о проекте (только своего).  
- `DELETE /projects/{project_id}` — удалить проект (каскадно удалит задачи проекта). 

### Задачи

Также требуют авторизации.

- `GET /tasks` — список задач. Поддерживает:
  - `project_id` — фильтр по проекту;
  - `status` — по булевому статусу (done/не done);
  - `min_priority`, `max_priority` — фильтр по приоритету;
  - `limit`, `offset` — пагинация. 
- `POST /tasks` — создать задачу:
  - тело включает `title`, `project_id`, опционально `description`, `priority`, `assigned_to_id`;  
  - если `assigned_to_id` не указан, задача назначается на текущего пользователя;
  - перед созданием проверяется, что `project_id` принадлежит текущему пользователю. 
- `GET /tasks/{task_id}` — получить задачу по id (только если назначена на текущего пользователя).  
- `PATCH /tasks/{task_id}` — частичное обновление (статус, приоритет, описание и т.п.).  
- `DELETE /tasks/{task_id}` — удалить задачу.

## Тестирование

Для тестов используется отдельная SQLite‑БД (`sqlite+aiosqlite:///./test.db`) и переопределённая зависимость `get_db`, чтобы полностью изолировать тесты от основной PostgreSQL.[6][5][7]

### Запуск тестов

```bash
pytest
```

Примеры уже реализованных тестов:

- `test_login_flow`:
  - регистрирует пользователя через `POST /users/`;
  - логинится через `POST /auth/login`;
  - проверяет, что вернулся валидный `access_token`.[1][4]
- В `conftest.py` есть фабрика `register_and_login`, которая:
  - регистрирует пользователя и логинится им;
  - возвращает JWT‑токен для использования в авторизованных запросах (например, `GET /projects`, `POST /tasks`).[8][1]

## Возможные улучшения

Идеи для развития проекта:

- Роли и права (например, `is_admin`, расшаренные проекты). 
- Enum‑статусы задач (`todo / in_progress / done`) вместо булевого поля. 
- Более подробная документация OpenAPI: описания полей, примеры, коды ошибок. 
- CI (GitHub Actions) для автоматического запуска тестов при каждом пуше.[9]

***

[1](https://fastapi.tiangolo.com/tutorial/testing/)
[2](https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e)
[3](https://berkkaraal.com/blog/2024/09/19/setup-fastapi-project-with-async-sqlalchemy-2-alembic-postgresql-and-docker/)
[4](https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/)
[5](https://github.com/seapagan/fastapi_async_sqlalchemy2_example)
[6](https://dev.to/whchi/testing-fastapi-with-async-database-session-1b5d)
[7](https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html)
[8](https://betterstack.com/community/guides/testing/pytest-fixtures-guide/)
[9](https://www.frugaltesting.com/blog/what-is-fastapi-testing-tools-frameworks-and-best-practices)
