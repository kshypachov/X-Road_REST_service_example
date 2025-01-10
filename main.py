from fastapi import FastAPI, Request, HTTPException, Depends, Header
import databases
from fastapi.responses import Response
import models.person
import logging
from utils.get_all_persons import get_all_persons_from_db
from utils.create_person import create_person_in_db
from utils.update_person import update_person_in_db
from utils.delete_person import delete_person_in_db
from utils.get_person import get_person_by_params_from_db
from pydantic import ValidationError
from utils.config_utils import load_config, get_database_url, configure_logging
import utils.validation
from utils import definitions

# Цей сервіс є частиною навчальних матеріалів для розробників системи "Трембіта".
# Сервіс як приклад логує всі HTTP-заголовки, які отримує з запитами.
# У промисловому сервісі слід передбачити логування службових заголовків системи "Трембіта".
# Перелік службових заголовків системи "Трембіта":
# Uxp-Client
# Uxp-Service
# Uxp-Purpose-Ids
# Uxp-Subject-Id


# Завантажуємо конфігурацію
try:
    config = load_config('config.ini')

    # Налаштовуємо логування
    configure_logging(config)

    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded")
    logger.debug("Debug message")

    # Отримуємо URL бази даних
    SQLALCHEMY_DATABASE_URL = get_database_url(config)
except ValueError as e:
    logging.critical(f"Failed to load configuration: {e}")
    exit(1)

# створюємо об'єкт database, який буде використовуватися для виконання запитів
database = databases.Database(SQLALCHEMY_DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    # коли програма запускається встановлюємо з'єднання з БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # коли програма зупиняється розриваємо з'єднання з БД
    await database.disconnect()


@app.get("/person")  # отримати дані про всіх людей, що містяться у базі заних
async def person_get_all(request: Request, queryId: str = None, userId: str = None):
    logger.debug("Початок обробки запиту GET /person")

    # Логування всіх заголовків
    headers = dict(request.headers)
    logger.info("Заголовки запиту:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Логування додаткових параметрів запиту Трембити
    if queryId:
        logger.info(f"Значення параметру запиту queryId: {queryId}")
    if userId:
        logger.info(f"Значення параметру запиту userId: {userId}")

    result = await get_all_persons_from_db(database)
    logger.debug("Обробку запиту GET /person завершено")
    return {"message": result}

@app.get("/person/{param}/{value}") # робимо пошук даних за одним з параметрів
async def person_get_by_parameter(param:str, value: str, request: Request, queryId: str = None, userId: str = None):
    logger.debug("Початок обробки запиту GET /person/" + str(param) + "/" + str(value))

    # Логування всіх заголовків
    headers = dict(request.headers)
    logger.info("Заголовки запиту:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Логування додаткових параметрів запиту Трембити
    if queryId:
        logger.info(f"Значення параметру запиту queryId: {queryId}")
    if userId:
        logger.info(f"Значення параметру запиту userId: {userId}")

    if not param.strip() or not value.strip():
        logger.warning("Один з переданих параметрів не містить значення")
        raise HTTPException(status_code=422, detail="Error in URL path, some values are missing")

    try:
        utils.validation.validate_parameter(param, value, models.person.PersonGet)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    search_dict = {param : value}
    result = await get_person_by_params_from_db(search_dict, database)
    return {"message": result}

@app.post("/person") # створюємо новий запис
async def person_post(request: Request, person: models.person.PersonCreate, queryId: str = None, userId: str = None):
    logger.debug("Початок обробки запиту POST /person/ " + str(person))

    # Логування всіх заголовків
    headers = dict(request.headers)
    logger.info("Заголовки запиту:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Логування додаткових параметрів запиту Трембити
    if queryId:
        logger.info(f"Значення параметру запиту queryId: {queryId}")
    if userId:
        logger.info(f"Значення параметру запиту userId: {userId}")

    result = await create_person_in_db(dict(person), database)
    logger.debug("Обробку запиту POST /person/  завершено")
    return {"message": result}

@app.put("/person") # оновлюємо запис
async def person_update(request: Request, person: models.person.PersonUpdate, queryId: str = None, userId: str = None):
    logger.debug("Початок обробки запиту PUT /person/ " + str(person))

    # Логування всіх заголовків
    headers = dict(request.headers)
    logger.info("Заголовки запиту:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Логування додаткових параметрів запиту Трембити
    if queryId:
        logger.info(f"Значення параметру запиту queryId: {queryId}")
    if userId:
        logger.info(f"Значення параметру запиту userId: {userId}")

    update_data = person.dict(exclude_none=True)
    result = await update_person_in_db(update_data, database)
    logger.debug("Обробку запиту PUT /person/  завершено")
    if result == 0:
        # немає даних для оновлення
        return Response(status_code = 204)
    return {"message": "Person updated successfully"}

@app.delete("/person/{param}/{value}")  # видаляємо запис, необхідно передати УНЗР для того щоб видалити людину
async def person_delete(param: str, value: str, request: Request, queryId: str = None, userId: str = None):
    logger.debug("Початок обробки запиту DELETE /person/" + str(param) + "/" + str(value))

    # Логування всіх заголовків
    headers = dict(request.headers)
    logger.info("Заголовки запиту:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Логування додаткових параметрів запиту Трембити
    if queryId:
        logger.info(f"Значення параметру запиту queryId: {queryId}")
    if userId:
        logger.info(f"Значення параметру запиту userId: {userId}")

    if not param.strip() or not value.strip():
        logger.warning("Один з переданих параметрів не містить значення")
        raise HTTPException(status_code=422, detail="Search parameter is missing in request")

    try:
        utils.validation.validate_parameter(param, value, models.person.PersonDelete)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    delete_person = {param : value}
    result = await delete_person_in_db(delete_person, database)
    logger.debug("Обробку запиту DELETE /person/" + str(param) + "/" + str(value) + " завершено")
    if result == 0:
        # немає даних для видаленя
        return Response(status_code = 204)
    return {"message": "Person deleted successfully"}

