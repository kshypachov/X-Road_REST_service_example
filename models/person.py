import enum
import sqlalchemy

from pydantic import BaseModel, Field, validator, ValidationError
from datetime import date
from typing import Optional, Union, Any

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

#Модель даних використовується для валідації даних що прийшли с запитом
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
        # Удаляем все символы "-" из строки для проверки цифр и длины
        digits_only = value.replace('-', '')

        if digits_only and (not digits_only.isdigit() or len(digits_only) != 14):
            raise ValueError('UNZR must be a 14 digit number')
        return value


class PersonCreate(PersonMainModel):
    pass


class PersonUpdate(PersonMainModel):
    pass


class PersonDelete(BaseModel):
    unzr: str

    @validator('unzr')
    def validate_unzr(cls, value):
        # Удаляем все символы "-" из строки для проверки цифр и длины
        digits_only = value.replace('-', '')

        if digits_only and (not digits_only.isdigit() or len(digits_only) != 14):
            raise ValueError('UNZR must be a 14 digit number')
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

#class PersonResponse(BaseModel):
#    status: bool
#    descr: str
#    result: Union[dict, None]  # Результат запроса в формате JSON


# Функция для валидации произвольного параметра
# def validate_parameter(param_name: str, param_value: Any) -> bool:
#     if param_name not in PersonMainModel.__fields__:
#         raise ValueError(f"Parameter '{param_name}' is not a valid field of PersonMainModel")
#
#     # Создаем временный словарь с проверяемым значением
#     temp_data = {param_name: param_value}
#
#     try:
#         # Валидируем временный объект модели
#         PersonMainModel(**temp_data)
#         return True
#     except Exception as e:
#         print(f"Validation error for {param_name}: {e}")
#         return False