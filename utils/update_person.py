from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select, update
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

# Function to update data in the database
async def update_person_in_db(update_data: dict, db: databases.Database):
    logger.info("Received data for update: %s", update_data)

    # Create a query to find the record in the database
    query = (
        select(
            Person.c.id,
        )
        .select_from(Person)
        .where(Person.c.unzr == str(update_data.get("unzr")))
    )
    person = await db.fetch_one(query)

    # If the record is not found
    if not person:
        logger.warning("Record with UNZR %s not found", str(update_data.get("unzr")))
        raise HTTPException(status_code=404, detail="Person not found")

    logger.info("Record found for update: %s", person)

    # Create a query to update the record
    update_query = (
        update(Person)
        .where(Person.c.id == person["id"])
        .values(**update_data)
    )

    try:
        result = await db.execute(update_query)
        if result == 0:
            logger.info("Record with ID %d did not require an update", person["id"])
            return result
        logger.info("Record with ID %d successfully updated", person["id"])
        return result
    except Exception as e:
        logger.error("Error while executing update query: %s", e)
        raise HTTPException(status_code=500, detail="Failed to update person")