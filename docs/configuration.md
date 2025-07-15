## Web Service Configuration

Web service configuration is performed in the "config.ini" and "alembic.ini" files.

If the web service was installed using a script, no additional configuration is required.

If the web service was installed manually, you need to edit these files as follows:

1. In the `alembic.ini` file, edit the following line:
  ```ini
  sqlalchemy.url = mariadb+mariadbconnector://user:pass@localhost/dbname
  ```
where:
- user – database user login;
- pass – password for this user;
- dbname – database name.

2. In the `config.ini` file, edit the `[database]` section, specifically the following parameters:

  ```ini
  db_type = mysql
  host = your_db_host
  port = your_db_port
  name = your_db_name
  username = your_db_user
  password = your_db_password
  ```

The configuration parameter values for the `config.ini` file are shown below:

   ```ini
   [database]
   # Type of database you are using. Possible values: mysql or postgres
   db_type = mysql
   
   # IP address or domain name of the database server
   host = your_db_host
   
   # Port through which the database connection is made. Default for MySQL is 3306
   port = your_db_port
   
   # Name of the database to connect to
   name = your_db_name
   
   # Username for database connection
   username = your_db_user
   
   # User password for database connection
   password = your_db_password
   
   [logging]
   # Path to the file where the log will be written
   filename = path/to/fastapi_trembita_service.log
   
   # filemode determines the mode in which the log file will be opened.
   # 'a' - append to existing file
   # 'w' - overwrite file each time the program starts
   filemode = a
   
   # format determines the format of log messages.
   # %(asctime)s - record creation time
   # %(name)s - logger name
   # %(levelname)s - logging level
   # %(message)s - message text
   # %(pathname)s - path to the file where the call was made
   # %(lineno)d - line number in the file where the call was made
   format = %(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s
   
   # dateformat determines the date format in log messages.
   # Possible formats can be:
   # %Y-%m-%d %H:%M:%S - 2023-06-25 14:45:00
   # %d-%m-%Y %H:%M:%S - 25-06-2023 14:45:00
   dateformat = %H:%M:%S
   
   # level determines the logging level. Most detailed is DEBUG, default is INFO
   # DEBUG - detailed information useful for debugging, logs request and response content
   # INFO - general information about program execution
   # WARNING - warnings about possible issues
   # ERROR - errors that prevented normal execution
   # CRITICAL - critical errors that lead to program termination
   level = DEBUG
   ```
##
Materials created with support from the EU Technical Assistance Project "Bangladesh e-governance (BGD)".