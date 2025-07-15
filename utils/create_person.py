from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import insert, exc
import logging
import pymysql

# Create a logger instance
logger = logging.getLogger(__name__)


# Function to create a new record in the database
async def create_person_in_db(person_data: dict, db: databases.Database):
    logger.info("Received data for creating a record in the database: %s", person_data)

    query = insert(Person).values(person_data).returning(Person.c.id)

    try:
        # Execute the database insert query
        record_id = await db.fetch_one(query)
        logger.info("Record created with ID: " + str(record_id))
        return record_id

    except exc.IntegrityError as ie:
        # Data integrity violation errors
        logger.error("Data integrity error during record creation: %s", ie)
        raise HTTPException(status_code=400, detail="Data integrity error")

    except pymysql.IntegrityError as pymyex:
        # Data integrity violation errors from PyMySQL
        logger.error("Data integrity error during record creation: %s", pymyex)
        raise HTTPException(status_code=400, detail="Data integrity error")

    except exc.SQLAlchemyError as sqle:
        # Other SQLAlchemy-related errors
        logger.error("Error while executing insert query: %s", sqle)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Other general errors
        logger.error("Unknown error during record creation: %s", e)
        raise HTTPException(status_code=500, detail="Unknown error")