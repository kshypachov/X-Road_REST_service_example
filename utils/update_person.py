from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import select, update
import logging

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)

# Функція для оновлення даних у БД
async def update_person_in_db(update_data: dict, db: databases.Database):
    logger.info("Отримані дані для оновлення: %s", update_data)

    # Створення запиту для пошуку запису у БД
    query = (
        select(
            Person.c.id,
        ).
        select_from(Person).
        where(Person.c.unzr == str(update_data.get("unzr"))))
    person = await db.fetch_one(query)

    # Якщо запис не знайдено
    if not person:
        logger.warning("Запис з UNZR %s не знайдено", str(update_data.get("unzr")))
        raise HTTPException(status_code=404, detail="Person not found")

    logger.info("Знайдено запис для оновлення: %s", person)

    # Створення запиту на оновлення даних
    update_query = (
        update(Person)
        .where(Person.c.id == person["id"])
        .values(**update_data)
    )

    try:
        result = await db.execute(update_query)
        if result == 0:
            logger.info("Запис з ID %d не потребував оновлення", person["id"])
            return result
        logger.info("Запис з ID %d успішно оновлено", person["id"])
        return result
    except Exception as e:
        logger.error("Помилка при виконання запиту на оновленння: %s", e)
        raise HTTPException(status_code=500, detail="Failed to update person")



