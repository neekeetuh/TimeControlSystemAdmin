import locale
import tkinter as tk
import calendar

from .Table import Table as tb
from models.standard_working_calendar import *
from models.work_day import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

"""
Класс StandardWorkingCalendarFrame является наследником tk.Frame, представляет собой экран, содержащий информацию о 
нормах рабочих часов для определённой даты(месяц и год) с набором кнопок для определённых действий с записями таблицы.
"""


class StandardWorkingCalendarFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        headings = ['Дата', 'Норма часов']
        self._table = tb(self, headings=headings, rows=self.get_data())
        self._table.pack()

        self._file_name = tk.Label(self, text='')
        self._file_name.pack()
        self._choose_file = tk.Button(self, text='Выбрать файл', command=self.read_dict_working_hours,
                                      background='lightblue')
        self._choose_file.pack()
        self._save_calendar = tk.Button(self, text='Составить рабочий календарь', command=self.insert_working_calendar,
                                        state='disabled', background='lightblue')
        self._save_calendar.pack()

        self._amount_of_working_hours_in_months = {}

        self._delete_button = tk.Button(self, text='Удалить запись', command=self.delete_record, background='lightblue')
        self._delete_button.pack()

    """
    Функция, делающая запрос данных из БД и возвращающая их в виде массива.
    """

    def get_data(self):
        data = []
        with db:
            for row in StandardWorkingCalendar.select():
                content = [
                    row.date,
                    row.standard_working_time
                ]
                data.append(content)
        return data

    """
    Команда, открывающая json файл стандартного рабочего календаря и создающая словарь с нормами рабочих часов за месяц.
    """

    def read_dict_working_hours(self):
        op = askopenfilename()
        if op.endswith('.json'):
            self._file_name['text'] = op
            with open(op, "r") as read_file:
                self._save_calendar['state'] = 'normal'
                working_calendar = json.load(read_file)
                self._amount_of_working_hours_in_months = {x: calendar.monthrange(working_calendar["year"], x)[1] * 8
                                                           for x
                                                           in
                                                           range(1, 13)}
                self._amount_of_working_hours_in_months['year'] = working_calendar['year']
                for month in working_calendar['months']:
                    for day in month["days"].split(","):
                        if day.find('*') == -1:
                            self._amount_of_working_hours_in_months[month["month"]] -= 8
                        else:
                            self._amount_of_working_hours_in_months[month["month"]] -= 1
        else:
            mb.showerror('Ошибка', 'Выберите файл в формате json')
            self.refresh()

    """
    Команда, считывающая данные из словаря, созданного в функции read_dict_working_hours, и производящая вставку
    считанных данных в таблицу БД.
    """

    def insert_working_calendar(self):
        working_calendar = []
        for i in range(1, 13):
            working_calendar.append(
                {'date': f"{calendar.month_name[i]}" + ' ' + f"{self._amount_of_working_hours_in_months['year']}",
                 'standard_working_time': self._amount_of_working_hours_in_months[i]})
        with db:
            try:
                StandardWorkingCalendar.insert_many(working_calendar).execute()
                self.refresh()
                mb.showinfo('Успешно', 'Рабочий календарь на ' + f"{self._amount_of_working_hours_in_months['year']}" +
                            ' год составлен и занесён в таблицу')
            except IntegrityError:
                mb.showerror('Ошибка', 'Рабочий календарь на указанный год уже составлен')

    """
    Функция, осуществляющая удаление записи из таблицы с помощью запроса на удаление в БД.
    """

    def delete_record(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                date = self._table.get_table().item(selection)['values'][0]
                try:
                    answer = mb.askyesno('Подтверждение', 'Вы действительно хотите удалить выбранную запись?')
                    if answer:
                        StandardWorkingCalendar.delete().where(
                            StandardWorkingCalendar.date == date).execute()
                        mb.showinfo('Успешно', 'Запись удалена')
                        self.refresh()
                except IntegrityError:
                    mb.showerror('Ошибка', 'На выбранную запись ссылаются записи из другой таблицы')
        else:
            mb.showerror('Ошибка', 'Выберите запись для удаления')

    """
    Функция для обновления экрана.
    """

    def refresh(self):
        parent = self.master
        self.destroy()
        parent.switch_frame(StandardWorkingCalendarFrame)
