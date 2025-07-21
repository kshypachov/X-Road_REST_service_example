#!/bin/bash

# Configuration variables
REPO_URL="https://github.com/kshypachov/X-Road_REST_service_example.git"
PROJECT_DIR="X-Road_REST_service_example"
VENV_DIR="venv"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_NAME="your_db_name"
DB_HOST="localhost" # Using localhost for installing MariaDB on this server
DB_PORT="3306"      # Default port for MariaDB
SERVICE_NAME="x-road_rest_service_example"
APP_MODULE="main:app" # Specify the correct application module

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y curl libmariadb-dev gcc python3 python3-venv python3-dev git

# Configure MariaDB repository
echo "Configuring MariaDB repository..."
curl -sS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash

# Install MariaDB server
echo "Installing MariaDB server..."
sudo apt-get install -y mariadb-server

# Start and enable MariaDB service
echo "Starting and enabling MariaDB..."
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Create database and user
echo "Creating database and user..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Clone the repository
echo "Cloning the repository..."
git clone $REPO_URL
cd $PROJECT_DIR

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate   # For Windows: venv\Scripts\activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure database connection
echo "Configuring database connection..."
sed -i "s/^sqlalchemy.url = .*/sqlalchemy.url = mariadb+mariadbconnector:\/\/$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT\/$DB_NAME/" alembic.ini
sed -i "s/^host = .*/host = $DB_HOST/" config.ini
sed -i "s/^port = .*/port = $DB_PORT/" config.ini
sed -i "s/^name = .*/name = $DB_NAME/" config.ini
sed -i "s/^username = .*/username = $DB_USER/" config.ini
sed -i "s/^password = .*/password = $DB_PASSWORD/" config.ini

# Create the database schema
echo "Creating database schema..."
alembic revision --autogenerate -m "Init migration"
alembic upgrade head

# Create a systemd unit file
echo "Creating systemd unit file..."
sudo bash -c "cat > /etc/systemd/system/$SERVICE_NAME.service" << EOL
[Unit]
Description=X-Road_REST_service_example
After=network.target

[Service]
User=$USER
WorkingDirectory=$PWD
ExecStart=$PWD/$VENV_DIR/bin/uvicorn $APP_MODULE --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and start the service
echo "Reloading systemd and starting the service..."
sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME
sudo systemctl enable $SERVICE_NAME

echo "Installation complete! The service has been started and enabled to launch on boot."