from models.person import person_table as Person
from fastapi import HTTPException
import databases
from sqlalchemy import delete
import logging


logger = logging.getLogger(__name__)

async def delete_person_in_db( person_data: dict, db: databases.Database):
    logger.info("Отримані данні для видалення: %s", person_data)

    query = (delete(Person).where(Person.c.UNZR == str(person_data.get("UNZR"))))

    try:
        status = await db.execute(query)
        logger.info("Кількість видаленних записів: %d", status)

        if status == 0:
            logger.warning("Запис з UNZR %s не знайдено", person_data.get("UNZR"))
            raise HTTPException(status_code=404, detail="Person not found")
        return status

    except Exception as e:
        logger.error("Помилка під час виконанні запиту на видалення: %s", e)
        raise