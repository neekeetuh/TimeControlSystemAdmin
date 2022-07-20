import tkinter as tk
from models.calculated_month_wage import *
from models.standard_working_calendar import *
from models.work_day import *

"""
Класс DataBaseFrame является наследником tk.Frame, представляет собой экран, содержащий кнопку для генерирования в БД
определённых таблиц.
"""


class DataBaseFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self._empty_label1 = tk.Label(self, text='', height=25)
        self._empty_label1.pack()
        self._generate_db_button = tk.Button(self, text='Сгенерировать таблицы в базе данных',
                                             command=self.generate_database, font=('Arial', 24), background='lightblue',
                                             pady=10, padx=10)
        self._generate_db_button.pack()

    """
    Команда, производящая запрос на создание таблиц в БД.
    """

    def generate_database(self):
        with db:
            db.create_tables([CalculatedMonthWage, Department, Employee, Position, StandardWorkingCalendar, WorkDay])
