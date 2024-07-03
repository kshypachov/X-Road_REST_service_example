from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select
import logging

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

# Функція для отримання всіх записів з БД
async def get_all_persons_from_db(db: databases.Database):
    logger.info("Запит на отримання всіх записів з БД")

    # Формуємо запит на отримання даних
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
        persons = await db.fetch_all(query)

        if not persons:
            logger.warning("Не знайдено жодного запису")
            raise HTTPException(status_code=404, detail="Person not found")

        logger.info("Отримано всі дані, що містяться у базі даних")
        return persons

    except HTTPException as http_error:
        logger.warning("Помилка HTTP: %s", http_error)
        raise http_error

    except databases.DatabaseError as db_error:
        logger.error("Помилка під час виконання запиту до бази даних: %s", db_error)
        raise HTTPException(status_code=500, detail="Failed to retrieve person from database")

    except Exception as e:
        logger.error("Помилка під час виконання запиту на отримання даних: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve person")
