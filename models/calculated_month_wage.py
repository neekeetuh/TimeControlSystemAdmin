from .employee import *

"""
Класс CalculatedMonthWage является наследником BaseModel, представляет собой таблицу расчёта зарплат из БД.
"""


class CalculatedMonthWage(BaseModel):
    employee_id = ForeignKeyField(Employee)
    date = CharField(max_length=100)
    summa = IntegerField()

    class Meta:
        db_table = "CalculatedMonthWages"
        primary_key = CompositeKey('employee_id', 'date')
