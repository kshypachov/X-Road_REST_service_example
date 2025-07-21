from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select, and_
import logging
from opentelemetry import trace

# Create a logger instance
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

# Function to search for records by any of the fields
async def get_person_by_params_from_db(params: dict, db: databases.Database):
    logger.info("Request to retrieve data with parameters: %s", params)

    # Create a list of conditions for the search
    conditions = []
    for key, value in params.items():
        if hasattr(Person.c, key):
            conditions.append(getattr(Person.c, key) == value)

    if not conditions:
        logger.warning("No search parameters provided")
        raise HTTPException(status_code=400, detail="No search parameters provided")

    # Create a database query to fetch data
    query = (
        select(
            Person.c.id,
            Person.c.name,
            Person.c.surname,
            Person.c.patronym,
            Person.c.dateOfBirth,
            Person.c.gender,
            Person.c.rnokpp,
            Person.c.passportNumber,
            Person.c.unzr,
        )
        .select_from(Person)
        .where(and_(*conditions))
    )

    try:
        # Create telemetry span for the SELECT query
        with tracer.start_as_current_span("DB: select persons by parameter") as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.operation", "SELECT")
            span.set_attribute("db.statement", str(query))
            span.set_attribute("db.table", Person.name)
            span.set_attribute("app.layer", "database")

            person = await db.fetch_all(query)

        if not person:
            logger.warning("No record found with parameters %s", params)
            raise HTTPException(status_code=404, detail="Person not found")

        logger.info("Retrieved record data: %s", person)
        return person

    except HTTPException as http_error:
        logger.warning("HTTP error occurred: %s", http_error)
        raise http_error

    except Exception as e:
        logger.error("Error while executing data retrieval query: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve person")