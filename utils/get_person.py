from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select, and_
import logging

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

# Функція для пошуку записів за будь-яким з полів
async def get_person_by_params_from_db(params: dict, db: databases.Database):
    logger.info("Запит на отримання даних з параметрами: %s", params)

    # Створюємо список умов для пошуку
    conditions = []
    for key, value in params.items():
        if hasattr(Person.c, key):
            conditions.append(getattr(Person.c, key) == value)

    if not conditions:
        logger.warning("Не надано жодного параметра для пошуку")
        raise HTTPException(status_code=400, detail="No search parameters provided")

# створюємо запит до БД для отримання даних
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
        person = await db.fetch_all(query)

        if not person:
            logger.warning("Запис з параметрами %s не знайдено", params)
            raise HTTPException(status_code=404, detail="Person not found")

        logger.info("Отримано дані наступного запису: %s", person)
        return person

    except HTTPException as http_error:
        logger.warning("Помилка HTTP: %s", http_error)
        raise http_error

    except Exception as e:
        logger.error("Помилка під час виконання запиту на отримання даних: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve person")
