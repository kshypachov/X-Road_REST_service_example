## Service Installation Using the Automatic Deployment Script

To automate the installation and setup of the web service, a script named `deploy.sh` has been created.

**This script:**

1. Installs the required system dependencies for the web service.
2. Clones the repository.
3. Creates and activates a virtual environment.
4. Installs Python dependencies.
5. Installs the MariaDB database server.
6. Configures the database.
7. Creates the database schema using Alembic.
8. Creates a systemd service unit file to run the web service.

**To install the web service using the script:**

1. Download the script:

```bash
wget https://raw.githubusercontent.com/kshypachov/X-Road_REST_service_example/master/x-road_rest_service_deploy.sh
```

2. Edit the `deploy.sh` script by replacing the values of `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_HOST`, and `DB_PORT` with your actual data, where:

- [DB_NAME] – name of the database;
- [DB_USER] – database user login;
- [DB_PASSWORD] – password for the specified user;
- [DB_HOST] – IP address of the host where the database is located;
- [DB_PORT] – port used to connect to the database.

The script will automatically create and configure the database using the provided parameters.

3. Make the script executable:

```bash
chmod +x x-road_rest_service_deploy.sh
```

4. Run the script:

```bash
./x-road_rest_service_deploy.sh
```

After the script finishes execution, the service will be automatically started and added to system startup.

The service will be configured automatically. For more details about configuration files, see the [configuration guide](./configuration.md).

---

Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".
