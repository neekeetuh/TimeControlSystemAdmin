from .department import *
from .position import *

"""
Класс Employee является наследником BaseModel, представляет собой таблицу сотрудников из БД.
"""


class Employee(BaseModel):
    id = PrimaryKeyField(unique=True, verbose_name='employee_id')
    surname = CharField(max_length=100)
    name = CharField(max_length=100)
    patronymic = CharField(max_length=100, null=True)
    email = CharField(max_length=100, null=True)
    phone_number = CharField(max_length=12)
    position_id = ForeignKeyField(Position)
    department_id = ForeignKeyField(Department)

    class Meta:
        db_table = "Employees"
