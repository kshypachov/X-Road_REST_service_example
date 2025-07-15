## Manual Service Removal

**To manually uninstall this web service, follow the steps below:**

### 1. Stop the web service:

```bash
sudo systemctl stop fastapi_trembita_service
```

### 2. Disable the service from autostart:

```bash
sudo systemctl disable fastapi_trembita_service
```

### 3. Remove the systemd unit file and reload the system configuration:

```bash
sudo rm /etc/systemd/system/fastapi_trembita_service.service
sudo systemctl daemon-reload
```

### 4. Delete the virtual environment and service files:

```bash
cd ..
sudo rm -rf FastAPI_trembita_service
```

### 5. Delete the database and user:
5.1.	Log into the MariaDB console:
```bash
sudo mysql
```
5.2.	Delete the database:
```sql
DROP DATABASE IF EXISTS your_db_name;
```
Where `your_db_name` is the name of the database created during web service installation.

5.3.	Delete the database user:
```sql
DROP USER IF EXISTS 'your_db_user'@'%';
```
Where `your_db_user` is the username created during web service installation.

5.4.	Exit the MariaDB console:
```sql
exit
```

### 6. Remove dependencies (optional):

```bash
sudo apt-get remove --purge -y curl libmariadb-dev gcc python3 python3-venv python3-dev git mariadb-server
sudo apt-get autoremove -y
```

After completing all steps, make sure there are no active processes or remaining files related to the project in the system.

---

Materials were prepared with the support of the international technical assistance project "Bangladesh e-governance (BGD)".