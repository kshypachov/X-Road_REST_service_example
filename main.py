from fastapi import FastAPI, Request, HTTPException, Depends, Header
import databases
from fastapi.responses import Response
import models.person
# from models.person import person_table
# from models.person import genderEnum
# from sqlalchemy import desc, func, select, insert
# from pydantic import BaseModel
# from utils.update_person import update_person_in_db
# from utils.delete_person import delete_person_in_db
# import asyncio
import logging
# import configparser
# from sqlalchemy.orm import Session
# from typing import Annotated
from utils.get_person import get_person_by_rnokpp_from_db
from utils.get_all_persons import get_all_persons_from_db
from utils.create_person import create_person_in_db
from utils.update_person import update_person_in_db
from utils.delete_person import delete_person_in_db
from utils.get_person import get_person_by_params_from_db
from pydantic import ValidationError
from utils.config_utils import load_config, get_database_url, configure_logging
import utils.validation

# Загружаем конфигурацию
try:
    config = load_config('config.ini')

    # Настраиваем логирование
    configure_logging(config)

    logger = logging.getLogger(__name__)
    logger.info("Running Urban Planning")

    # Получаем URL базы данных
    SQLALCHEMY_DATABASE_URL = get_database_url(config)
except ValueError as e:
    logging.critical(f"Failed to load configuration: {e}")
    exit(1)

# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(SQLALCHEMY_DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()


@app.get("/person")  # отримати данні про всіх людей що містяться у базі заних
async def person_get_all(request: Request):
    logger.debug("Початок обробки запиту GET /person")
    header = request.headers.get("uxp-transaction-id", "None")
    logger.info("Значення хедеру uxp-transaction-id: " + header)

    result = await get_all_persons_from_db(database)
    logger.debug("Обробку запиту GET /person завершено")
    return result


# @app.get("/person/rnokpp/{rnokpp_code}")  #Пошук людини за кодом РНОКПП
# async def person_get_by_rnokpp_code(rnokpp_code: str, request: Request):
#     logger.debug("Початок обробки запиту GET /person/rnokpp/" + rnokpp_code)
#     header = request.headers.get("uxp-transaction-id", "None")
#     logger.info("Значення хедеру uxp-transaction-id: " + header)
#
#     try:
#         validated_code = models.person.PersonGet(RNOKPP=rnokpp_code)
#     except ValueError as e:
#         logging.error("Помилка валідації RNOKPP при виконанні запиту GET")
#         raise HTTPException(status_code=400, detail=str(e))
#
#     result = await get_person_by_rnokpp_from_db(validated_code.RNOKPP, database)
#
#     logger.debug("Обробку запиту GET /person/rnokpp/" + rnokpp_code + " завершено")
#     return result


@app.get("/person/{param}/{value}")
async def person_get_by_parameter(param:str, value: str):

    try:
        utils.validation.validate_parameter(param, value)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    search_dict = {param : value}

    result = await get_person_by_params_from_db(search_dict, database)

    print (result)

    return result

@app.post("/person")
async def person_post(request: Request, person: models.person.PersonCreate):
    header = request.headers.get("uxp-transaction-id", "None")
    logger.info("Значення хедеру uxp-transaction-id: " + header)

    logger.debug("Початок обробки запиту POST /person/ " + str(person))
    result = await create_person_in_db(dict(person), database)
    logger.debug("Обробку запиту POST /person/  завершено")
    return {"message": result}

@app.put("/person")
async def person_update(request: Request, person: models.person.PersonUpdate):
    header = request.headers.get("uxp-transaction-id", "None")
    logger.info("Значення хедеру uxp-transaction-id: " + header)

    logger.debug("Початок обробки запиту PUT /person/ " + str(person))
    update_data = person.dict(exclude_none=True)
    result = await update_person_in_db(update_data, database)
    logger.debug("Обробку запиту PUT /person/  завершено")
    if result == 0:
        return Response(status_code = 204)
    return {"message": "Person updated successfully"}


@app.delete("/person")  # Необхідно передати УНЗР для того щоб видалити людину
async def person_delete(request: Request, person: models.person.PersonDelete):
    header = request.headers.get("uxp-transaction-id", "None")
    logger.info("Значення хедеру uxp-transaction-id: " + header)

    logger.debug("Початок обробки запиту DELETE /person/ " + str(person))
    delete_person = person.dict(exclude_none=True)
    result = await delete_person_in_db(delete_person, database)
    logger.debug("Обробку запиту DELETE /person/  завершено")
    if result == 0:
        return Response(status_code = 204)
    return {"message": "Person deleted successfully"}
