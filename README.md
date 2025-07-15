# Synchronous REST Service Compatible with the "X-Road" System

The REST service described in this manual is developed in Python using the FastAPI framework and is compatible with the "X-Road" system.

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.10+, based on standard asynchronous calls.

This service is designed to retrieve information about data objects (users) from a database (registry) and manage their status, including handling requests to search, retrieve, create, update, and delete objects.

To demonstrate integration with the "X-Road" system, a [web client](https://github.com/MadCat-88/Trembita_Py_R_SyncCli) was developed to work with this web service.

## Software Requirements
| Software       | Version   | Note                                                                                                                                                                                                               |
|:---------------|:---------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ubuntu Server  | 24.04     | Recommended virtual machine characteristics:<br/> CPU: 1 <br/> RAM: 512 MB                                                                                                                                        |
| Python         | **3.10!** | Installed automatically via script.<br/>You can also install it manually by selecting the appropriate installation type.<br/>**Important!** If Python version is below 3.10, the service will not work.           |
| MariaDB        | 10.5+     | Installed automatically via script.<br/>Can also be installed manually by selecting the appropriate installation type.                                                                                             |
| Git            |           | Required for cloning the repository                                                                                                                                                                                |

## Dependencies

The software dependencies of the web service are listed in the `requirements.txt` file.

## Project Structure

The project has the following structure:

```
X-Road_REST_service_example/
├── main.py                # Application entry point
├── config.ini             # Project configuration
├── alembic.ini            # DB migrations configuration
├── utils/
│   ├── validations.py     # Field validation
│   ├── update_person.py   # Update DB record
│   ├── get_person.py      # Search DB record by criteria
│   ├── get_all_persons.py # Retrieve all DB records
│   ├── delete_person.py   # Delete DB record
│   ├── create_person.py   # Create DB record
│   └── config_utils.py    # Read configuration file
├── models/
│   └── person.py          # Data models
├── migrations/
│   └── env.py             # Alembic model connection
├── docs/                  # Deployment documentation
├── requirements.txt       # Web service dependencies
├── README.md              # Documentation
├── deploy.sh              # Installation automation script
├── remove.sh              # Script to remove the service and clean the system
```

## Service Installation

The service can be installed using an automatic installation script or manually. It can also run in Docker.

- [Automatic installation script](./docs/script_installation.md)
- [Manual installation](./docs/manual_installation.md)
- [Service configuration](./docs/configuration.md)
- [Deploying the web service with Docker](./docs/docker_installation.md)

## Populating the Database with Test Records

For convenient testing of the developed web service, the database should be populated with test records.  
#A dedicated script was created for this purpose. Installation and usage are described [here](https://github.com/MadCat-88/Trembita_PutFakeData_Rest).

## Service Administration

### Starting the Web Service

To start the web service, run the following command:

```bash
sudo systemctl start x-road_rest_service_example
```

### Accessing API Documentation

Once the web service is running, you can access the automatically generated **API documentation** at:

- Swagger UI: http://[server-address]:8000/docs  
- ReDoc: http://[server-address]:8000/redoc

### Checking Service Status

```bash
sudo systemctl status x-road_rest_service_example
```

### Stopping the Web Service

```bash
sudo systemctl stop x-road_rest_service_example
```

### Removing the Web Service

To remove the web service and all related components, use the `remove.sh` script.  
This script will stop and delete the web service, remove the virtual environment, cloned repository, and system dependencies.

To execute the script:

1. Make the file executable:

```bash
chmod +x remove.sh
```

2. Run the script:

```bash
./remove.sh
```

You can also manually remove the service according to the relevant [instructions](/docs/delete.md).

### Viewing the Event Log

By default, the service event log is saved in the file `x-road_rest_service_example.log`.

Logging parameters are configured in the `config.ini` file. More details are available in the [configuration guide](/docs/configuration.md).

To view the service event log:

```bash
journalctl -u x-road_rest_service_example -f
```

### HTTPS Configuration

Instructions for setting up HTTPS using a reverse proxy are provided [here](./docs/https_nginx_reverse_proxy.md).

## Using the Service

The web service provides 5 methods to manage records of fictional users (Person) in the database:

- [Create a new record](./docs/using.md#person-post)
- [Retrieve all records from the DB](./docs/using.md#person-get-all)
- [Update a record by unique identifier (UNZR)](/docs/using.md#person-update)
- [Retrieve a record by search criteria](./docs/using.md#person-get-by-parameter)
- [Delete a record by unique identifier (UNZR)](./docs/using.md#person-delete)

After installing the service, the database is empty.  
To demonstrate its capabilities, the first step is to create records in the DB. You can do this using the [web client](https://github.com/MadCat-88/Trembita_Py_R_SyncCli), the [Person Post method](./docs/using.md#person-post), or the [test data population script](./README.md#populating-the-database-with-test-records).

## Contribution

If you want to contribute to the project, please fork the repository and submit a Pull Request.

## License

This project is licensed under the MIT License.

##

Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".