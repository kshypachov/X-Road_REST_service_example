from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select
import logging
from opentelemetry import trace

# Create a logger instance
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

# Function to retrieve all records from the database
async def get_all_persons_from_db(db: databases.Database):
    logger.info("Request to retrieve all records from the database")

    # Prepare the query to fetch data
    query = select(
        Person.c.id,
        Person.c.name,
        Person.c.surname,
        Person.c.patronym,
        Person.c.dateOfBirth,
        Person.c.gender,
        Person.c.rnokpp,
        Person.c.passportNumber,
        Person.c.unzr,
    ).select_from(Person)

    try:
        # Create telemetry span for the SELECT query
        with tracer.start_as_current_span("DB: select all persons") as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.operation", "SELECT")
            span.set_attribute("db.statement", str(query))
            span.set_attribute("db.table", Person.name)
            span.set_attribute("app.layer", "database")

            persons = await db.fetch_all(query)

        if not persons:
            logger.warning("No records found")
            raise HTTPException(status_code=404, detail="Person not found")

        logger.info("Successfully retrieved all records from the database")
        return persons

    except HTTPException as http_error:
        logger.warning("HTTP error occurred: %s", http_error)
        raise http_error

    # except databases.DatabaseError as db_error:
    #     logger.error("Database error occurred while executing the query: %s", db_error)
    #     raise HTTPException(status_code=500, detail="Failed to retrieve person from database")

    except Exception as e:
        logger.error("Unexpected error occurred while retrieving data: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve person")