from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import delete
import logging
from opentelemetry import trace

# Create a logger instance
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


# Function to delete a record from the database.
# Requires a dictionary in the form {"unzr": "11111111-11111"}
async def delete_person_in_db(person_data: dict, db: databases.Database):
    logger.info("Received data for deletion: %s", person_data)

    query = delete(Person).where(Person.c.unzr == str(person_data.get("unzr")))

    try:
        with tracer.start_as_current_span("DB: delete person by UNZR") as span:
            span.set_attribute("db.system", "mysql")
            span.set_attribute("db.operation", "DELETE")
            span.set_attribute("db.statement", str(query))
            span.set_attribute("db.table", Person.name)
            span.set_attribute("app.layer", "database")

            status = await db.execute(query)

        logger.info("Number of records deleted: %d", status)

        if status == 0:
            logger.warning("Record with UNZR %s not found", person_data.get("unzr"))
            raise HTTPException(status_code=404, detail="Person not found")
        return status

    except Exception as e:
        logger.error("Error while executing delete query: %s", e)
        raise