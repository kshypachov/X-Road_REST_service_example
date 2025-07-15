# Manual Service Installation

It is also possible to install the web service manually without using an installation script.  
To get started, you need a clean Ubuntu system — all required packages and repositories will be installed during the setup process.

**To manually install this web service, follow the steps below:**

### 1. Install the required packages:

```bash
sudo apt-get update
sudo apt-get install -y curl libmariadb-dev gcc python3 python3-venv python3-dev git
```

**Important:** If your Python version is below 3.10, the service will not work.

### 2. Add the MariaDB repository:

```bash
curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash
```

### 3. Install the MariaDB database server:

```bash
sudo apt-get update
sudo apt-get install -y mariadb-server
```

### 4. Start MariaDB and enable it to start on boot:

```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### 5. Verify that MariaDB is running:

```bash
sudo systemctl status mariadb
```

**Note:** If the database is running, proceed to the next steps.  
Otherwise, review previous steps for any errors.

### 6. Create the database and user:

6.1. Log into the MariaDB console:

```bash
sudo mysql
```

6.2. Create the database:
```sql
CREATE DATABASE IF NOT EXISTS your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Where `your_db_name` is your desired database name.

6.3. Create the user:
```sql
CREATE USER IF NOT EXISTS 'your_db_user'@'%' IDENTIFIED BY 'your_db_password';
```
Where:
- `your_db_user` is the database username;
- `your_db_password` is the password for that user.

6.4. Grant the user full privileges on the database, replacing `your_db_name` and `your_db_user` accordingly:
```sql
GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_db_user'@'%';
```

6.5. Apply the privileges:
```sql
FLUSH PRIVILEGES;
```

The database and user have been successfully created.

6.6. Exit the MariaDB console:

```bash
exit
```

### 7. Clone the repository:

```bash
git clone https://github.com/kshypachov/FastAPI_trembita_service.git
```

### 8. Navigate to the project directory:

```bash
cd FastAPI_trembita_service
```

### 9. Create a virtual environment:

```bash
python3 -m venv venv
```

### 10. Activate the virtual environment:

```bash
source venv/bin/activate
```

### 11. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 12. Configure the web service according to the [configuration guide](/docs/configuration.md)

### 13. Create the database structure:

13.1. Create the initial migration:

```bash
alembic revision --autogenerate -m "Init migration"
```

13.2. Apply the migrations to create the database schema:

```bash
alembic upgrade head
```

### 14. Create a `systemd` unit file to run the web service:

**Note:** Before executing the command, ensure you're in the `FastAPI_trembita_service` directory by running `pwd`.

Create the unit file:

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

### 15. Reload the systemd configuration:

```bash
sudo systemctl daemon-reload
```

### 16. Enable the service to start on boot:

```bash
sudo systemctl enable fastapi_trembita_service
```

---

Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".