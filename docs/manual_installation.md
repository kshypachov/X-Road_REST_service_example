# Посібник з встановлення сервісу вручну

## Опис 
Цей посібник допоможе пройти процесс встановлення сервісу вручну. Для почтаку потрібно мати чисту систему Ubuntu, 
всі необхідні пакети та репозиторії будуть підключені пізніше.

## Загальні вимоги
- Python 3.10+
- Git (для клонування репозиторію)
- MariaDB 10.5+
- Ubuntu Server 24.04

## Встановлення сервісу

### 1. Встановлення залежностей
Для початку потрібно встановити всі необхідні пакети. Виконайте наступні команди для встановлення Python 3.10 і супутніх інструментів:

```bash
sudo apt-get update
sudo apt-get install -y curl libmariadb-dev gcc python3 python3-venv python3-dev git
```
- Примітка: Якщо версія Python нижче 3.10, сервіс працювати не буде. Інші пакети необхідні для коректної роботи з базою даних та репозиторієм.

### 2. Встановлення MariaDB

#### Налаштування репозиторію MariaDB
Щоб встановити MariaDB версії 10.5 або вище, потрібно додати офіційний репозиторій:
```bash
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
```
#### Встановлення MariaDB сервера
```bash
sudo apt-get update
sudo apt-get install -y mariadb-server
```
#### Запуск і додавання MariaDB в автозапуск
Запустіть та додайте MariaDB до автозапуску:
```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

#### Перевірка статусу MariaDB
Перевірте, чи працює MariaDB:
```bash
sudo systemctl start mariadb
```
Якщо базу даних запущено, можна рухатись до наступних кроків.
В інакшому випадку потрібно перевірити чи не буде зроблено помилку в одному з попередніх кроків.

### 3. Створення бази даних і користувача

1. Увійдіть у консоль MariaDB
```bash
sudo mysql
```

2. Створіть базу даних, замінивши your_db_name на бажану назву бази даних:
```sql
CREATE DATABASE IF NOT EXISTS your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Створіть користувача, замінивши your_db_user та your_db_password на ваші значення:
```sql
CREATE USER IF NOT EXISTS 'your_db_user'@'%' IDENTIFIED BY 'your_db_password';
```

4. Надайте користувачу повні права на базу даних, замінивши your_db_user на ваше значення:
```sql
GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_db_user'@'%';
```

5. Примусово оновіть привілеї:
```sql
FLUSH PRIVILEGES;
```
Тепер у вас є база даних та користувач, і можна рухатися до налаштування та запуску сервісу.

### 4. Клонування репозиторію та налаштування віртуального середовища

1. Клонуйте репозиторій проєкту:
```bash
git clone https://github.com/kshypachov/FastAPI_trembita_service.git
```

2.	Перейдіть до директорії проєкту:
```bash
cd FastAPI_trembita_service
```

3.	Створіть віртуальне середовище:
```bash
python3 -m venv venv
```

4. Активуйте віртуальне середовище:
```bash
source venv/bin/activate
```

5. Встановіть залежності для проєкту:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 5. Конфігурування сервісу
#### Редагування конфігураційних файлів

Відредагуйте наступні файли:

- У файлі `alembic.ini` відредагуйте рядок:
  ```ini
  sqlalchemy.url = mariadb+mariadbconnector://user:pass@localhost/dbname
  ```
- У файлі `config.ini` відредагуйте секцію `[database]`:
  ```ini
  db_type = mysql
  host = your_db_host
  port = your_db_port
  name = your_db_name
  username = your_db_user
  password = your_db_password
  ```

- Опис полів `config.ini` :

   ```ini
   [database]
   # Тип бази даних, яку ви використовуєте. Можливі значення: mysql або postgres
   db_type = mysql
   
   # IP-адреса або доменне ім'я сервера бази даних
   host = your_db_host
   
   # Порт, через який здійснюється підключення до бази даних. За замовчуванням для MySQL це 3306
   port = your_db_port
   
   # Ім'я бази даних, до якої потрібно підключитися
   name = your_db_name
   
   # Ім'я користувача для підключення до бази даних
   username = your_db_user
   
   # Пароль користувача для підключення до бази даних
   password = your_db_password
   
   [logging]
   # Шлях до файлу, куди буде записуватися лог
   filename = path/to/client.log
   
   # filemode визначає режим, в якому буде відкритий файл логування.
   # 'a' - дописувати до існуючого файлу
   # 'w' - перезаписувати файл кожен раз при старті програми
   filemode = a
   
   # format визначає формат повідомлень логування.
   # %(asctime)s - час створення запису
   # %(name)s - ім'я логгера
   # %(levelname)s - рівень логування
   # %(message)s - текст повідомлення
   # %(pathname)s - шлях до файлу, звідки було зроблено виклик
   # %(lineno)d - номер рядка у файлі, звідки було зроблено виклик
   format = %(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s
   
   # dateformat визначає формат дати в повідомленнях логування.
   # Можливі формати можуть бути такими, як:
   # %Y-%m-%d %H:%M:%S - 2023-06-25 14:45:00
   # %d-%m-%Y %H:%M:%S - 25-06-2023 14:45:00
   dateformat = %H:%M:%S
   
   # level визначає рівень логування. Найбільш детальний це DEBUG, за замовчуванням INFO
   # DEBUG - докладна інформація, корисна для відлагодження роботи, логується вміст запитів та відповідей
   # INFO - загальна інформація про стан виконання програми
   # WARNING - попередження про можливі проблеми
   # ERROR - помилки, які завадили нормальному виконанню
   # CRITICAL - критичні помилки, що призводять до завершення програми
   level = DEBUG
   ```

### 6. Створення структури бази даних

1.	Створіть початкову міграцію:
```bash
alembic revision --autogenerate -m "Init migration"
```

2.	Застосуйте міграції для створення структури бази даних:
```bash
alembic upgrade head
```

### 7. Налаштування та запуск сервісу як systemd-сервіс
Перевірте за допомогою команди `pwd` що ви знаходитесь у директорії `FastAPI_trembita_service`. 
Створіть systemd unit-файл для запуску сервісу:

```bash
sudo bash -c "cat > /etc/systemd/system/fastapi_trembita_service.service" << EOL
[Unit]
Description=FastAPI Trembita Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$PWD
ExecStart=$PWD/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL
```
#### Перезапуск systemd та запуск сервісу

1.	Перезавантажте конфігурацію systemd:
```bash
sudo systemctl daemon-reload
```

2.	Запустіть сервіс:
```bash
sudo systemctl start fastapi_trembita_service
```

3. Додайте сервіс до автозапуску:
```bash
sudo systemctl enable fastapi_trembita_service
```

4.	Перевірте статус сервісу:
```bash
sudo systemctl status fastapi_trembita_service
```

### 8. Логування та моніторинг
Для перевірки логів сервісу використовуйте команду:
```bash
journalctl -u fastapi_trembita_service -f
```
Також сервіс пиши лог файл, його розташування вказане у конфігураційному файлі `config.ini`

#### Завершення
Сервіс запущено! Після запуску сервера ви можете отримати доступ до автоматичної документації API за наступними адресами:

- Swagger UI: http://[адреса серверу]:8000/docs
- ReDoc: http://[адреса серверу]:8000/redoc





















