## Інструкція для видалення проєкту

### 1. Зупинка сервісу
Для початку потрібно зупинити активний сервіс:
```bash
sudo systemctl stop fastapi_trembita_service
```

### 2. Видалення сервісу із автозапуску
Видаліть сервіс з автозапуску:
```bash
sudo systemctl disable fastapi_trembita_service
```

### 3. Видалення systemd unit-файлу
Видаліть файл сервісу, щоб уникнути залишкових слідів у системі:
```bash
sudo rm /etc/systemd/system/fastapi_trembita_service.service
```
Перезавантажте конфігурацію systemd:
```bash
sudo systemctl daemon-reload
```

### 4. Видалення віртуального середовища та файлів проєкту
Перейдіть до директорії, де знаходиться проєкт, і видаліть її:
```bash
cd ..
sudo rm -rf FastAPI_trembita_service
```

### 5. Видалення бази даних та користувача
1.	Увійдіть у консоль MariaDB:
```bash
sudo mysql
```
2.	Видаліть базу даних (замініть your_db_name на ім’я вашої бази):
```sql
DROP DATABASE IF EXISTS your_db_name;
```

3.	Видаліть користувача (замініть your_db_user на ім’я користувача):
```sql
DROP USER IF EXISTS 'your_db_user'@'%';
```
4.	Вийдіть із консолі MariaDB:
```sql
exit
```

### 6. Видалення залежностей (опціонально)
```bash
sudo apt-get remove --purge -y curl libmariadb-dev gcc python3 python3-venv python3-dev git mariadb-server
sudo apt-get autoremove -y
```

### 7. Перевірка стану
Переконайтеся, що жодних активних процесів чи файлів, пов’язаних із проєктом, більше немає в системі.
