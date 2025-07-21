import logging
from models.person import PersonGet
from typing import Any
from fastapi import HTTPException
from opentelemetry import trace

# Tracer instance
tracer = trace.get_tracer(__name__)

# Create a logger instance
logger = logging.getLogger(__name__)

def validate_parameter(param_name: str, param_value: Any, validation_model: Any):
    with tracer.start_as_current_span("Validate Parameter") as span:
        span.set_attribute("param.name", param_name)
        span.set_attribute("param.value", str(param_value))
        span.set_attribute("validation.model", validation_model.__name__)

        logger.info(f"Validating parameter '{param_name}' with value '{param_value}'")

        if param_name not in validation_model.__fields__:
            error_msg = f"Parameter '{param_name}' is not a valid field of {validation_model.__name__}"
            logger.error(error_msg)

            span.set_attribute("validation.error", error_msg)
            span.set_status(trace.status.Status(trace.status.StatusCode.ERROR, description=error_msg))

            raise HTTPException(status_code=422, detail=error_msg)

        # Create a temporary dictionary with the value to be validated
        temp_data = {param_name: param_value}

        try:
            # Validate the temporary model object
            validation_model(**temp_data)
            logger.debug(f"Parameter '{param_name}' with value '{param_value}' is valid.")

        except Exception as e:
            error_msg = f"Validation error for parameter '{param_name}' with value '{param_value}': {e}"
            logger.error(error_msg)
            span.set_attribute("validation.error", str(e))
            span.set_status(trace.status.Status(trace.status.StatusCode.ERROR, description=str(e)))
            raise HTTPException(status_code=422, detail=error_msg)
