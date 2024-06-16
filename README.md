# Проект на FastAPI з підтримкою системи Трембіта

## Опис
Цей проект представляє собою веб-сервіс, розроблений з використанням FastAPI. FastAPI - це сучасний, швидкий (високопродуктивний) web-фреймворк для побудови API з Python 3.10+ на основі стандартних асинхронних викликів. Проект підтримує систему Трембіта (логування заголовків).

## Вимоги
- Python 3.10+
- Git (для клонування репозиторію)
- MariaDB 10.5+

## Встановлення

### Клонування репозиторію

```bash
git clone https://github.com/kshypachov/FastAPI_trembita_service.git
cd FastAPI_trembita_service
```

### Встановлення за допомогою скрипта deploy.sh

Ми додали скрипт `deploy.sh` для автоматизації процесу встановлення. Скрипт виконує наступні кроки:
1. Встановлює системні залежності.
2. Клонує репозиторій.
3. Створює та активує віртуальне середовище.
4. Встановлює залежності Python.
5. Налаштовує конфігурацію бази даних.
6. Створює структуру бази даних за допомогою Alembic.
7. Створює `systemd` сервіс для запуску застосунку.

#### Використання скрипта deploy.sh

1. Відредагуйте скрипт `deploy.sh`, замінивши значення змінних `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, `DB_PORT`, `SERVICE_NAME` та `APP_MODULE` на ваші реальні дані.
2. Зробіть файл виконуваним:

   ```bash
   chmod +x deploy.sh
   ```

3. Запустіть скрипт:

   ```bash
   ./deploy.sh
   ```

### Ручне встановлення

#### Створення та активація віртуального середовища

```bash
python3 -m venv venv
source venv/bin/activate   # Для Windows: venv\Scripts\activate
```

#### Встановлення залежностей

```bash
sudo apt-get install -y libmariadb-dev gcc python3-dev 
pip install -r requirements.txt
```

#### Створення БД

Цей сервіс використовує MySQL (MariaDB). Створіть базу даних та користувача на сервері СКБД.

#### Конфігурування сервісу

Відредагуйте наступні файли:

- У файлі `alembic.ini` відредагуйте строчку:
  ```ini
  sqlalchemy.url = mariadb+mariadbconnector://user:pass@localhost/dbname
  ```
- У файлі `config.ini` відредагуйте секцію `[database]`:
  ```ini
  host = your_db_host
  port = your_db_port
  name = your_db_name
  username = your_db_user
  password = your_db_password
  ```

#### Створення таблиць

Створенням та обслуговуванням структури БД займається Alembic. Для створення структури БД виконайте наступні команди:

```bash
alembic revision --autogenerate -m "Init migration"
alembic upgrade head
```

## Запуск застосунку

### Запуск сервера

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```
Тут `main` - це ім'я файлу, що містить об'єкт FastAPI `app`. Відкрийте браузер і перейдіть за адресою http://[адреса серверу]:8000.

## Структура проекту

Структура проекту виглядає наступним чином:

```
FastAPI_trembita_service/
├── main.py                # Точка входу застосунку
├── config.ini             # Конфігурація проекту
├── alembic.ini            # Конфігурація міграцій БД
├── utils/
│   ├── validations.py     # Валідація параметрів
│   ├── update_person.py   # Оновлення запису у БД
│   ├── get_person.py      # Пошук запису у БД за критерієм
│   ├── get_all_persons.py # Отримання всіх записів БД
│   ├── delete_person.py   # Видалення запису з БД
│   ├── create_person.py   # Створення запису у БД
│   └── config_utils.py    # Зчитування конфігураційного файлу
├── models/
│   └── person.py          # Моделі даних
├── migrations/
│   └── env.py             # Підключення моделей для Alembic
├── requirements.txt       # Залежності проекту
├── README.md              # Документація
├── deploy.sh              # Скрипт для автоматизації встановлення
```

## Документація

Після запуску сервера ви можете отримати доступ до автоматичної документації API за наступними адресами:

- Swagger UI: http://[адреса серверу]:8000/docs
- ReDoc: http://[адреса серверу]:8000/redoc

## Розгортання

Для розгортання на сервері використовуйте один з наступних методів:

- **Docker**: Створіть Dockerfile для контейнеризації застосунку.
- **Gunicorn**: Використовуйте Gunicorn у поєднанні з Uvicorn для запуску застосунку у виробничому середовищі.

### Приклад запуску з Gunicorn:

```bash
gunicorn -k uvicorn.workers.UvicornWorker main:app
```

## Внесок

Якщо ви хочете зробити свій внесок у проект, будь ласка, створіть форк репозиторію і відправте пулреквест.

## Ліцензія

Цей проект ліцензується відповідно до умов MIT License.
