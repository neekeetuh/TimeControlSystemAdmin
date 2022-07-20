from .base import *

"""
Класс StandardWorkingCalendar является наследником BaseModel, представляет собой таблицу стандартных рабочих календарей 
из БД.
"""


class StandardWorkingCalendar(BaseModel):
    date = CharField(max_length=100, primary_key=True)
    standard_working_time = IntegerField()

    class Meta:
        db_table = "StandardWorkingCalendars"
