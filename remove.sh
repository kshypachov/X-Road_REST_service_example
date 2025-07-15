#!/bin/bash

# Configuration variables
PROJECT_DIR="X-Road_REST_service_example"
VENV_DIR="venv"
SERVICE_NAME="x-road_rest_service_example"
CONFIG_FILE="config.ini"

# Function to read values from config.ini
function get_config_value() {
    local section=$1
    local key=$2
    local config_file=$3
    local value=$(awk -F "=" '/\['"$section"'\]/{a=1}a==1&&$1~/'"$key"'/{gsub(/[ \t]+$/, "", $2); print $2; exit}' $config_file)
    echo $value
}

# Retrieve database parameters from config.ini
DB_NAME=$(get_config_value "database" "name" $CONFIG_FILE)
DB_USER=$(get_config_value "database" "username" $CONFIG_FILE)
DB_PASSWORD=$(get_config_value "database" "password" $CONFIG_FILE)

# Ensure the script is run from inside the FastAPI project directory
if [ "$(basename "$PWD")" != "$PROJECT_DIR" ]; then
    echo "Please run this script from the $PROJECT_DIR directory."
    exit 1
fi

# Stop and remove the systemd service
echo "Stopping and removing the systemd service..."
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo rm /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

# Remove the virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Removing the virtual environment..."
    rm -rf "$VENV_DIR"
else
    echo "Virtual environment not found."
fi

# Go up one directory to delete the cloned repository
cd ..

# Delete the cloned repository
if [ -d "$PROJECT_DIR" ]; then
    echo "Removing the cloned repository..."
    rm -rf "$PROJECT_DIR"
else
    echo "Cloned repository not found."
fi

# Delete the database and user
echo "Deleting the database and user..."
sudo mysql -e "DROP DATABASE IF EXISTS $DB_NAME;"
sudo mysql -e "DROP USER IF EXISTS '$DB_USER'@'%';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "Removal complete!"