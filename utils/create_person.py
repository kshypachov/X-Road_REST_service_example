from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import insert, exc
import logging
import pymysql

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)


# функція для створення нового запису у бд
async def create_person_in_db(person_data: dict, db: databases.Database):
    logger.info("Отримано дані для створення запису у базі даних: %s", person_data)

    query = insert(Person).values(person_data).returning(Person.c.id)

    try:
        # виконуємо запит до БД на створення
        record_id = await db.fetch_one(query)
        logger.info("Створено запис з ID: " + str(record_id))
        return record_id

    except exc.IntegrityError as ie:
        # Помилки цілісності даних
        logger.error("Помилка цілісності даних під час створення запису: %s", ie)
        raise HTTPException(status_code=400, detail="Data integrity error")

    except pymysql.IntegrityError as pymyex:
        # Помилки цілісності даних
        logger.error("Помилка цілісності даних під час створення запису: %s", pymyex)
        raise HTTPException(status_code=400, detail="Data integrity error")

    except exc.SQLAlchemyError as sqle:
        # Інші помилки SQLAlchemy
        logger.error("Помилка під час виконання запиту на створення: %s", sqle)
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Інші загальні помилки
        logger.error("Невідома помилка під час створення запису: %s", e)
        raise HTTPException(status_code=500, detail="Unknown error")
