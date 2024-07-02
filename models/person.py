import enum
import sqlalchemy

from pydantic import BaseModel, Field, validator, ValidationError
from datetime import date, datetime
from typing import Optional, Union, Any
import re


metadata = sqlalchemy.MetaData()


class genderEnum(str, enum.Enum):
    male = "male"
    female = "female"

#Модель для взаємодії з базою даних через ORM
person_table = sqlalchemy.Table(
    "person",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column("surname", sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column("patronym", sqlalchemy.String(128)),
    sqlalchemy.Column("dateOfBirth", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("gender", sqlalchemy.Enum(genderEnum), nullable=False),
    sqlalchemy.Column("rnokpp", sqlalchemy.String(128), unique=True, nullable=False, index=True),
    sqlalchemy.Column("passportNumber", sqlalchemy.String(128), unique=True, nullable=False),
    sqlalchemy.Column("unzr", sqlalchemy.String(128), unique=True, nullable=False),
)

#Модель даних використовується для валідації даних що прийшли з запитом
class PersonMainModel(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    surname: str = Field( min_length=1, max_length=128)
    patronym: str = Field(None, max_length=128)
    dateOfBirth: date
    gender: str
    rnokpp: str
    passportNumber: str
    unzr: str

    @validator('dateOfBirth')
    def validate_date_of_birth(cls, value):
        if value and value > date.today():
            raise ValueError('dateOfBirth cannot be in the future')
        return value

    @validator('name', 'surname', 'patronym')
    def validate_name(cls, value):
        if value and not all(char.isalpha() for char in value):
            raise ValueError('Names must contain only alphabetic characters without space')
        return value

    @validator('gender')
    def validate_gender(cls, value):
        if value and value not in ['male', 'female']:
            raise ValueError('Gender must be either "male" or "female"')
        return value

    @validator('rnokpp')
    def validate_rnokpp(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError('RNOKPP must be a 10 digit number')
        return value

    @validator('passportNumber')
    def validate_pasport_num(cls, value):
        if value and (not value.isdigit() or len(value) != 9):
            raise ValueError('passportNum must be a 9 digit number')
        return value

    @validator('unzr')
    def validate_unzr(cls, value):
        # Перевірка формата
        if not re.match(r'^\d{8}-\d{5}$', value):
            raise ValueError('UNZR must be in the format YYYYMMDD-XXXXC')

        # Розділ на частини
        date_part, code_part = value.split('-')
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:])

        # Перевірка правильності дати
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError('Invalid date in UNZR')

        # Перевірка кода
        code = int(code_part[:4])
        if not (0 <= code <= 9999):
            raise ValueError('Code in UNZR must be in the range from 0000 to 9999')

        # Перевірка контрольної цифри
        control_digit = int(code_part[4])
        if not (0 <= control_digit <= 9):
            raise ValueError('Last symbol of UNZR is not a digit 0..9')

        return value


class PersonCreate(PersonMainModel):
    pass


class PersonUpdate(PersonMainModel):
    pass


class PersonDelete(BaseModel):
    unzr: str

    @validator('unzr')
    def validate_unzr(cls, value):
        # Перевірка формата
        if not re.match(r'^\d{8}-\d{5}$', value):
            raise ValueError('UNZR must be in the format YYYYMMDD-XXXXC')

        # Розділ на частини
        date_part, code_part = value.split('-')
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:])

        # Перевірка правильності дати
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError('Invalid date in UNZR')

        # Перевірка кода
        code = int(code_part[:4])
        if not (0 <= code <= 9999):
            raise ValueError('Code in UNZR must be in the range from 0000 to 9999')

        # Перевірка контрольної цифри
        control_digit = int(code_part[4])
        if not (0 <= control_digit <= 9):
            raise ValueError('Last symbol of UNZR is not a digit 0..9')

        return value


class PersonGet (PersonMainModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    surname: Optional[str] = Field(None, min_length=1, max_length=128)
    patronym: Optional[str] = Field(None, max_length=128)
    dateOfBirth: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, max_length=128)
    rnokpp: Optional[str] = Field(None, max_length=128)
    passportNumber: Optional[str] = Field(None, max_length=128)
    unzr : Optional[str] = Field(None, max_length=128)
