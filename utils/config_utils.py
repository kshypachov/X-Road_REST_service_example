import configparser
import os
import logging

# Створюється екземпляр класу logger
logger = logging.getLogger(__name__)


# Функція для зчитування конфігураційного файлу
def load_config(file_path: str, defaults: dict = None) -> configparser.ConfigParser:
    config = configparser.ConfigParser(defaults=defaults, interpolation=None)

    # Перевіряємо USE_ENV_CONFIG, і якщо true, не зчитуємо файл конфігурації
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        logger.info("Skipping config file loading, using environment variables only.")
    else:
        # Зчитуємо конфігураційний файл тільки якщо USE_ENV_CONFIG не true
        if not config.read(file_path):
            logger.error(f"Configuration file {file_path} not found or is empty.")
            raise FileNotFoundError(f"Configuration file {file_path} not found or is empty.")

    return config


# Функція для отримання значення параметрів з конфіг файлу або з перемінної оточення
def get_config_param(config: configparser.ConfigParser, section: str, param: str, env_var: str = None, default: str = None) -> str:
    # Если используется только переменные окружения
    if os.getenv("USE_ENV_CONFIG", "false").lower() == "true":
        env_value = os.getenv(env_var)
        if env_var and env_value is not None:
            return env_value
        else:
            return default  # Возвращаем default, если переменной окружения нет

    # Если используется конфигурационный файл
    if config.has_option(section, param):
        return config.get(section, param)
    else:
        return default  # Возвращаем default, если параметра нет в конфиге

# Функція для формування url строки для підключення до бд
def get_database_url(config: configparser.ConfigParser) -> str:
    db_user = get_config_param(config, 'database', 'username', 'DB_USER')
    db_password = get_config_param(config, 'database', 'password', 'DB_PASSWORD')
    db_host = get_config_param(config, 'database', 'host', 'DB_HOST')
    db_name = get_config_param(config, 'database', 'name', 'DB_NAME')

    missing_params = []
    if db_user is None:
        missing_params.append("DB_USER")
    if db_password is None:
        missing_params.append("DB_PASSWORD")
    if db_host is None:
        missing_params.append("DB_HOST")
    if db_name is None:
        missing_params.append("DB_NAME")

    if missing_params:
        missing_params_str = ", ".join(missing_params)
        logger.error(f"Не вистачає наступних параметрів для підключення до бази даних: {missing_params_str}")
        raise ValueError(f"Missing database connection parameters: {missing_params_str}")

    return f"mysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"


# Функція для налаштування логування
def configure_logging(config: configparser.ConfigParser):
    log_filename = get_config_param(config, 'logging', 'filename', 'LOG_FILENAME', default=None)
    log_filemode = get_config_param(config, 'logging', 'filemode', 'LOG_FILEMODE', default=None)
    log_format = get_config_param(config, 'logging', 'format', 'LOG_FORMAT', default=None)
    log_datefmt = get_config_param(config, 'logging', 'dateformat', 'LOG_DATEFORMAT', default=None)
    log_level = get_config_param(config, 'logging', 'level', 'LOG_LEVEL', default="info").upper()

    # Якщо log_filename пустий, то виводимо логи в консоль (stdout)
    if not log_filename:
        log_filename = None

    logging.basicConfig(
        filename=log_filename,  # Якщо None, то логи будуть виводитись в stdout
        filemode=log_filemode,
        format=log_format,
        datefmt=log_datefmt,
        level=getattr(logging, log_level, logging.DEBUG)
    )