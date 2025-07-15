import logging
from models.person import PersonGet
from typing import Any
from fastapi import HTTPException

# Create a logger instance
logger = logging.getLogger(__name__)

def validate_parameter(param_name: str, param_value: Any, validation_model: Any):
    logger.info(f"Validating parameter '{param_name}' with value '{param_value}'")

    if param_name not in validation_model.__fields__:
        logger.error(f"Parameter '{param_name}' is not a valid field of PersonMainModel")
        raise HTTPException(status_code=422, detail=f"Parameter '{param_name}' is not a valid field")

    # Create a temporary dictionary with the value to be validated
    temp_data = {param_name: param_value}

    try:
        # Validate the temporary model object
        validation_model(**temp_data)
        logger.debug(f"Parameter '{param_name}' with value '{param_value}' is valid.")

    except Exception as e:
        logger.error(f"Validation error for parameter '{param_name}' with value '{param_value}': {e}")
        raise HTTPException(status_code=422, detail=f"Validation error for parameter '{param_name}' with value '{param_value}': {e}")