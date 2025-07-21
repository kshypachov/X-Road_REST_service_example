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
from utils.config_utils import (
    load_config,
    get_database_url,
    configure_logging,
    load_telemetry_settings,
    configure_telemetry,
    instrument_app_with_telemetry)
import utils.validation
from utils import definitions

# This service is part of the training materials for developers working with the "X-Road" system.
# As an example, the service logs all HTTP headers received with each request.
# In production-grade services, only official "X-Road" headers should be logged.


# Load configuration
try:
    config = load_config('config.ini')

    # Configure logging
    configure_logging(config)

    telemetry_settings = load_telemetry_settings(config)
    configure_telemetry(telemetry_settings)

    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded")


    # Get the database URL
    SQLALCHEMY_DATABASE_URL = get_database_url(config)
except ValueError as e:
    logging.critical(f"Failed to load configuration: {e}")
    exit(1)

# Create the database object that will be used for executing queries
database = databases.Database(SQLALCHEMY_DATABASE_URL)

app = FastAPI()
try:
    instrument_app_with_telemetry(app, telemetry_settings)
except Exception as e:
    logger.error(f"Error while loading instrument_app_with_telemetry: {e}")


@app.on_event("startup")
async def startup():
    # On startup, connect to the database
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # On shutdown, disconnect from the database
    await database.disconnect()


@app.get("/person")  # Get data about all persons in the database
async def person_get_all(request: Request, queryId: str = None, userId: str = None):
    logger.debug("Start handling GET /person request")

    # Log all headers
    headers = dict(request.headers)
    logger.info("Request headers:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Log additional Trembita parameters
    if queryId:
        logger.info(f"Query parameter 'queryId': {queryId}")
    if userId:
        logger.info(f"Query parameter 'userId': {userId}")

    result = await get_all_persons_from_db(database)
    logger.debug("GET /person request handled")
    return {"message": result}


@app.get("/person/{param}/{value}")  # Search person data by one parameter
async def person_get_by_parameter(param: str, value: str, request: Request, queryId: str = None, userId: str = None):
    logger.debug("Start handling GET /person/" + str(param) + "/" + str(value))

    # Log all headers
    headers = dict(request.headers)
    logger.info("Request headers:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Log additional Trembita parameters
    if queryId:
        logger.info(f"Query parameter 'queryId': {queryId}")
    if userId:
        logger.info(f"Query parameter 'userId': {userId}")

    if not param.strip() or not value.strip():
        logger.warning("One of the parameters is missing a value")
        raise HTTPException(status_code=422, detail="Error in URL path, some values are missing")

    try:
        utils.validation.validate_parameter(param, value, models.person.PersonGet)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    search_dict = {param: value}
    result = await get_person_by_params_from_db(search_dict, database)
    return {"message": result}


@app.post("/person")  # Create a new person record
async def person_post(request: Request, person: models.person.PersonCreate, queryId: str = None, userId: str = None):
    logger.debug("Start handling POST /person/ " + str(person))

    # Log all headers
    headers = dict(request.headers)
    logger.info("Request headers:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Log additional Trembita parameters
    if queryId:
        logger.info(f"Query parameter 'queryId': {queryId}")
    if userId:
        logger.info(f"Query parameter 'userId': {userId}")

    result = await create_person_in_db(dict(person), database)
    logger.debug("POST /person request handled")
    return {"message": result}


@app.put("/person")  # Update an existing person record
async def person_update(request: Request, person: models.person.PersonUpdate, queryId: str = None, userId: str = None):
    logger.debug("Start handling PUT /person/ " + str(person))

    # Log all headers
    headers = dict(request.headers)
    logger.info("Request headers:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Log additional Trembita parameters
    if queryId:
        logger.info(f"Query parameter 'queryId': {queryId}")
    if userId:
        logger.info(f"Query parameter 'userId': {userId}")

    update_data = person.dict(exclude_none=True)
    result = await update_person_in_db(update_data, database)
    logger.debug("PUT /person request handled")
    if result == 0:
        # No data was updated
        return Response(status_code=204)
    return {"message": "Person updated successfully"}


@app.delete("/person/{param}/{value}")  # Delete a person record using UNZR
async def person_delete(param: str, value: str, request: Request, queryId: str = None, userId: str = None):
    logger.debug("Start handling DELETE /person/" + str(param) + "/" + str(value))

    # Log all headers
    headers = dict(request.headers)
    logger.info("Request headers:")
    for header_key, header_value in headers.items():
        logger.info(f"    {header_key}: {header_value}")

    # Log additional Trembita parameters
    if queryId:
        logger.info(f"Query parameter 'queryId': {queryId}")
    if userId:
        logger.info(f"Query parameter 'userId': {userId}")

    if not param.strip() or not value.strip():
        logger.warning("One of the parameters is missing a value")
        raise HTTPException(status_code=422, detail="Search parameter is missing in request")

    try:
        utils.validation.validate_parameter(param, value, models.person.PersonDelete)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    delete_person = {param: value}
    result = await delete_person_in_db(delete_person, database)
    logger.debug("DELETE /person/" + str(param) + "/" + str(value) + " request handled")
    if result == 0:
        # No data was deleted
        return Response(status_code=204)
    return {"message": "Person deleted successfully"}