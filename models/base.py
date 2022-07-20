from connection_db.connection_PostgreSQL_DataBase import *

"""
Класс BaseModel содержит в себе стандартные свойства для моделей.
"""


class BaseModel(Model):
    class Meta:
        order_by = id
        database = db
