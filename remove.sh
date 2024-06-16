#!/bin/bash

# Змінні для конфігурації
PROJECT_DIR="FastAPI_trembita_service"
VENV_DIR="venv"
SERVICE_NAME="fastapi_trembita_service"

# Перевірка, чи скрипт запускається з папки FastAPI_trembita_service
if [ "$(basename "$PWD")" != "$PROJECT_DIR" ]; then
    echo "Будь ласка, запустіть цей скрипт з директорії $PROJECT_DIR."
    exit 1
fi

# Зупинка та видалення системного сервісу
echo "Зупинка та видалення системного сервісу..."
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo rm /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

# Видалення віртуального середовища
if [ -d "$VENV_DIR" ]; then
    echo "Видалення віртуального середовища..."
    rm -rf "$VENV_DIR"
else
    echo "Віртуальне середовище не знайдено."
fi

# Перехід на один рівень вище для видалення клонованого репозиторію
cd ..

# Видалення клонованого репозиторію
if [ -d "$PROJECT_DIR" ]; then
    echo "Видалення клонованого репозиторію..."
    rm -rf "$PROJECT_DIR"
else
    echo "Клонований репозиторій не знайдено."
fi

echo "Видалення завершено!"