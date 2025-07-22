# Barter Platform

## Описание проекта
Платформа для обмена товарами и услугами между пользователями.

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/nex-kex/Barter-Platform.git
```
### 2. Настройки
#### Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
```
```bash
venv\Scripts\activate    # Windows
```

#### Установка зависимостей
##### Установка Poetry (если не установлен)
```bash
pip install poetry
```
##### Установка зависимостей
```bash
poetry install
```
Активация виртуального окружения
```bash
poetry shell
```
#### Настройка окружения
Создайте файл `.env` в корне проекта по примеру `.env.example` с содержанием:

```
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DB_NAME=имя_бд
DB_USER=пользователь_бд
DB_PASSWORD=пароль_бд
DB_HOST=localhost
DB_PORT=5432
```

#### Миграции
Примените миграции
```bash
python manage.py migrate
```

#### Создание суперпользователя 
Для удобного взаимодействия с [панелью администратора](http://127.0.0.1:8000/admin/) можно создать суперпользователя.
```bash
python manage.py createsuperuser
```

#### Заполнение базы тестовыми данными
Для заполнения БД тестовыми данными выполните команду
```bash
python manage.py loaddata ads_fixtures.json
```

## Запуск сервера
Запустите сервер выполнив команду в терминале:
```bash
python manage.py runserver
```

```bash
python3 manage.py runserver # Linux/macOS
```

Для остановки сервера используйте `Ctrl+C` в терминале

## Тестирование 
Для запуска тестов выполните команду
```bash
coverage run --source='.' manage.py test
```

Для просмотра отчёта о покрытии тестами выполните команду
```bash
coverage report -m
```
