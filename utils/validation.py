import logging
from models.person import PersonGet
from typing import Any
from fastapi import HTTPException

# створюється екземпляр классу логер
logger = logging.getLogger(__name__)


# Валідація назви параметру та значення
def validate_parameter(param_name: str, param_value: Any):
    logger.info(f"Validating parameter '{param_name}' with value '{param_value}'")

    if param_name not in PersonGet.__fields__:
        logger.error(f"Parameter '{param_name}' is not a valid field of PersonMainModel")
        raise HTTPException(status_code=422, detail=f"Parameter '{param_name}' is not a valid field")

    # Створюємо тимчасовий словник з значенням, що перевіряється
    temp_data = {param_name: param_value}

    try:
        # Валідуємо тимчасовий об'єкт моделі
        PersonGet(**temp_data)
        logger.debug(f"Parameter '{param_name}' with value '{param_value}' is valid.")

    except Exception as e:
        logger.error(f"Validation error for parameter '{param_name}' with value '{param_value}': {e}")
        raise HTTPException (status_code=422, detail=f"Validation error for parameter '{param_name}' with value '{param_value}': {e}")
