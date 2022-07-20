import datetime as dt
from models.work_day import *
from models.calculated_month_wage import *
from tkinter import messagebox as mb
from .Table import *

"""
Класс WorkDaysFrame является наследником tk.Frame, представляет собой экран с таблицей рабочих дней из БД и кнопкой для
удаления записей.
"""


class WorkDaysFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        headings = ['ID сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Номер телефона', 'Время начала смены',
                    'Время окончания смены']
        self._table = Table(self, headings=headings, rows=self.get_data())
        self._table.pack()

        self._delete_button = tk.Button(self, text='Удалить запись', command=self.delete_record, background='lightblue')
        self._delete_button.pack()

    """
    Команда для отмены действия.
    """

    def cancel_action(self):
        self.refresh()

    """
    Функция, делающая запрос данных из БД и возвращающая их в виде массива.
    """

    def get_data(self):
        data = []
        with db:
            for workday in WorkDay.select().order_by(WorkDay.start_time):
                content = [
                    workday.employee_id,
                    workday.employee_id.surname,
                    workday.employee_id.name,
                    workday.employee_id.patronymic,
                    workday.employee_id.phone_number,
                    workday.start_time,
                    workday.end_time,
                ]
                data.append(content)
        return data

    """
    Функция, осуществляющая удаление записи из таблицы с помощью запроса на удаление в БД.
    """

    def delete_record(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                employee_id = self._table.get_table().item(selection)['values'][0]
                start_time_str = self._table.get_table().item(selection)['values'][5]
                start_time = dt.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
                try:
                    answer = mb.askyesno('Подтверждение', 'Вы действительно хотите удалить выбранную запись?')
                    if answer:
                        WorkDay.delete().where(
                            WorkDay.employee_id == employee_id, WorkDay.start_time == start_time).execute()
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
        parent.switch_frame(WorkDaysFrame)
