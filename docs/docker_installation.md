# Deploying the Web Service in Docker

## Requirements

| Software        | Version    | Notes                         |
|:----------------|:----------:|-------------------------------|
| MariaDB         | **10.5+**  |                               |
| Docker          | **20.10+** |                               |
| Docker Compose  |   10.5+    | If planning to use it         |
| Git             |            | For cloning the repository    |

## Environment Variables

The web service supports configuration via environment variables.

Below are the main parameters:

- `USE_ENV_CONFIG`: Enables the use of environment variables for configuration. If set to `true`, the web service will use environment variables instead of a config file.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Password for connecting to the database.
- `DB_HOST`: Database host address.
- `DB_NAME`: Database name.
- `LOG_FILENAME`: Log file name. If empty, logs will be printed to the console (stdout).
- `LOG_LEVEL`: Logging level (e.g., `info`, `debug`).
- `LOG_FILEMODE`: Log file mode (e.g., `a` — append, `w` — overwrite).

## Building the Docker Image

To build the Docker image, follow these steps:

1. Clone the repository:
```bash
wget https://raw.githubusercontent.com/kshypachov/X-Road_REST_service_example/master/deploy.sh
```
2. Navigate to the web service directory:
```bash
cd X-Road_REST_service_example
```
3. Run the following command in the project root directory:
```bash
sudo docker build -t my-fastapi-app .
```

This command will build a Docker image named `my-fastapi-app` using the Dockerfile in the current directory.

## Creating the Database for the Service

Although the container includes Alembic, which can create the database structure, running it directly from the container is not convenient.  
Therefore, it is recommended to create the database and its structure manually.

To create the database and its structure:

1. Install MariaDB according to steps 2–5 of the [manual installation guide](./manual_installation.md#2-додати-репозиторій-mariadb).

2. Create the database and user as described in step 6 of the [manual installation guide](./manual_installation.md#6-створити-базу-даних-та-користувача-для-цього-необхідно).

3. Create the table structure by executing the following command:

```bash
sudo mysql -e "USE your_db_name; CREATE TABLE IF NOT EXISTS \`person\` (
  \`id\` int(11) NOT NULL AUTO_INCREMENT,
  \`name\` varchar(128) NOT NULL,
  \`surname\` varchar(128) NOT NULL,
  \`patronym\` varchar(128) DEFAULT NULL,
  \`dateOfBirth\` date NOT NULL,
  \`gender\` enum('male','female') NOT NULL,
  \`rnokpp\` varchar(128) NOT NULL,
  \`passportNumber\` varchar(128) NOT NULL,
  \`unzr\` varchar(128) NOT NULL,
  PRIMARY KEY (\`id\`),
  UNIQUE KEY \`passportNumber\` (\`passportNumber\`),
  UNIQUE KEY \`unzr\` (\`unzr\`),
  UNIQUE KEY \`ix_person_rnokpp\` (\`rnokpp\`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
COMMIT;"
```
Where `your_db_name` is the name of the database created in the previous step.

## Running and Using the Container with Environment Variables

To run the container with the web service:

```bash
sudo docker run -it --rm -p 8000:8000 \
    -e USE_ENV_CONFIG=true \
    -e DB_USER=myuser \
    -e DB_PASSWORD=mypassword \
    -e DB_HOST=mydbhost \
    -e DB_NAME=mydatabase \
    -e LOG_LEVEL=info \
    -e LOG_FILENAME="" \
    my-fastapi-app
```

Where:
- The `-p 8000:8000` flag maps port 8000 on the local machine to port 8000 inside the container.
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME` configure database access.
- Setting `LOG_FILENAME=""` will output logs to the console (stdout).

**Note:** If the database is hosted on the same machine as the web service, you must provide the host machine’s IP address in `DB_HOST`. `localhost` or `127.0.0.1` will not work in this case. You must also allow external connections to the database.

If you plan to configure the service entirely using environment variables, make sure `USE_ENV_CONFIG=true`.

Example:
```bash
sudo docker run -it --rm -p 8000:8000 \
    -e USE_ENV_CONFIG=true \
    -e DB_USER=myuser \
    -e DB_PASSWORD=mypassword \
    -e DB_HOST=mydbhost \
    -e DB_NAME=mydatabase \
    -e LOG_LEVEL=debug \
    my-fastapi-app
```

## Running and Using the Container with a Configuration File

You can also run the web service container using a configuration file instead of environment variables.  
To do so, create a `config.ini` file in the web service directory and mount it into the container:

```bash
sudo docker run -it --rm -p 8000:8000 \
    -v $(pwd)/config.ini:/app/config.ini \
    my-fastapi-app
```

Here, the `-v $(pwd)/config.ini:/app/config.ini` flag mounts your local `/app/config.ini` file into the container.

**Example `config.ini` file:**

```ini
[database]
db_type = mysql
username = myuser
password = mypassword
host = mydbhost
name = mydatabase

[logging]
filename = /var/log/app.log
filemode = a
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
dateformat = %Y-%m-%d %H:%M:%S
level = info
```

If the `USE_ENV_CONFIG` variable is unset or set to `false`, the service will use the configuration file instead.  
Make sure the file is available in the container as shown above.

## Viewing Logs

If logs are configured to be output to the console, you can view them with:

```bash
docker logs <container_id>
```

If logs are stored in a file (via the `LOG_FILENAME` variable or config file), you can mount a local directory for logs as follows:

```bash
docker run -it --rm -p 8000:8000 \
    -e LOG_FILENAME="/var/log/app.log" \
    -v $(pwd)/logs:/var/log \
    my-fastapi-app
```

Where the `-v $(pwd)/logs:/var/log` flag mounts your local logs directory into the container.

---

Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".