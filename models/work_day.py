from .employee import *

"""
Класс WorkDay является наследником BaseModel, представляет собой таблицу рабочих дней из БД.
"""


class WorkDay(BaseModel):
    employee_id = ForeignKeyField(Employee)
    start_time = DateTimeField(formats='DD.MM.YYYY HH:MM')
    end_time = DateTimeField(null=True, formats='DD.MM.YYYY HH:MM')

    class Meta:
        db_table = "WorkDays"
        primary_key = CompositeKey('employee_id', 'start_time')
