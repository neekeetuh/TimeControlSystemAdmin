from .base import *

"""
Класс Position является наследником BaseModel, представляет собой таблицу должностей из БД.
"""


class Position(BaseModel):
    id = PrimaryKeyField(unique=True, verbose_name='position_id')
    title = CharField(max_length=100)
    wage = IntegerField()

    class Meta:
        db_table = "Positions"
