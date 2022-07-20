from .base import *

"""
Класс Department является наследником BaseModel, представляет собой таблицу отделов из БД.
"""


class Department(BaseModel):
    id = PrimaryKeyField(unique=True, verbose_name='department_id')
    address = CharField(max_length=100, unique=True, verbose_name='department_address')

    class Meta:
        db_table = "Departments"
