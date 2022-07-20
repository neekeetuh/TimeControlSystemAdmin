import locale
import calendar
import datetime as dt
from models.work_day import *
from models.standard_working_calendar import *
from models.calculated_month_wage import *
from tkinter import messagebox as mb
from .Table import *

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

"""
Класс CalculatedMonthWagesFrame является наследником tk.Frame, представляет собой экран, содержащий информацию о
расчётах зарплат сотрудников за определённую дату(месяц и год) с набором кнопок для определённых действий с записями
таблицы.
"""


class CalculatedMonthWagesFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        headings = ['ID сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Номер телефона', 'Дата', 'Сумма']
        self._table = Table(self, headings=headings, rows=self.get_data())
        self._table.pack()

        months = [
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь'
        ]
        self._month_entry_label = tk.Label(self, text='Месяц:')
        self._month_entry = ttk.Combobox(self, values=months)
        self._month_entry_label.pack()
        self._month_entry.pack()
        self._year_entry_label = tk.Label(self, text='Год:')
        self._year_entry_text = tk.StringVar()
        self._year_entry = tk.Entry(self, textvariable=self._year_entry_text)
        self._year_entry_label.pack()
        self._year_entry.pack()

        self._empty_label = tk.Label(self)
        self._empty_label.pack()

        self._calc_button = tk.Button(self, text='Рассчитать зарплаты сотрудников',
                                      command=self.calculate_and_insert_wages, background='lightblue')
        self._calc_button.pack()

        self._delete_button = tk.Button(self, text='Удалить запись', command=self.delete_record, background='lightblue')
        self._delete_button.pack()

    """
    Функция, делающая запрос данных из БД и возвращающая их в виде массива.
    """

    def get_data(self):
        data = []
        with db:
            for row in CalculatedMonthWage.select():
                content = [
                    row.employee_id,
                    row.employee_id.surname,
                    row.employee_id.name,
                    row.employee_id.patronymic,
                    row.employee_id.phone_number,
                    row.date,
                    row.summa
                ]
                data.append(content)
        return data

    """
    Функция, расчитывающая количество часов, наработанных определённым сотрудником за указанный месяц и год. Параметр
    employee_id является идентификатором сотрудника, для которого нужно произвести расчёт. Параметр month - месяц, за
    который нужно произвести расчёт. Параметр year - год, за который нужно произвести расчёт.
    """

    @staticmethod
    def timedelta_calc(employee_id, month, year):
        delta = dt.timedelta()
        with db:
            workdays_query = WorkDay.select().where(WorkDay.employee_id == employee_id,
                                                    WorkDay.start_time.year == int(year),
                                                    WorkDay.start_time.month == list(calendar.month_name).index(month))
            for elem in workdays_query:
                start = dt.datetime.strptime(elem.start_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                end = dt.datetime.strptime(elem.end_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                diff = end - start
                delta += diff
        return delta.total_seconds() / 3600

    """
    Функция, расчитывающая заработную плату сотрудника за определённый месяц и год. Параметр employee_id является 
    идентификатором сотрудника, для которого нужно произвести расчёт. Параметр month - месяц, за который нужно 
    произвести расчёт. Параметр year - год, за который нужно произвести расчёт.
    """

    def wage_calc(self, employee_id, month, year):
        with db:
            wage_query = Position.select().join(Employee).where(Employee.id == employee_id)
            work_time = StandardWorkingCalendar.get(
                StandardWorkingCalendar.date == f"{month}" + ' ' + f"{year}")
            summa = 0
            for el in wage_query:
                summa = self.timedelta_calc(employee_id, month, year) / work_time.standard_working_time * el.wage
        return summa

    """
    Команда, производящая вставку данных о рассчитанных зарплатах всех сотрудников за выбранный месяц и год.
    """

    def calculate_and_insert_wages(self):
        displayed_month = str(self._month_entry.get())
        displayed_year = str(self._year_entry.get())
        is_valid = False
        can_insert = True
        with db:
            if self._month_entry.get() and self._year_entry.get():
                for date in StandardWorkingCalendar.select(StandardWorkingCalendar.date):
                    if date.date == f"{displayed_month}" + ' ' + f"{displayed_year}":
                        is_valid = True
                        break
                if is_valid:
                    employees_query = Employee.select()
                    calc_month_wages_query = CalculatedMonthWage.select(CalculatedMonthWage.date).distinct()
                    for el in calc_month_wages_query:
                        if el.date == f"{displayed_month}" + ' ' + f"{displayed_year}":
                            can_insert = False
                            break
                    if can_insert:
                        for employee in employees_query:
                            CalculatedMonthWage.insert(employee_id=employee.id,
                                                       date=f"{displayed_month}" + ' ' + f"{displayed_year}",
                                                       summa=self.wage_calc(employee.id, displayed_month,
                                                                            displayed_year)).execute()
                        mb.showinfo('Успешно', 'Зарплаты сотрудников успешно рассчитаны и занесены в таблицу')
                        self.refresh()
                    else:
                        mb.showerror("Ошибка", "Зарплаты на прошлый месяц уже рассчитаны")
                else:
                    mb.showerror('Ошибка', 'Календарь на эту дату не был загружен')
            else:
                mb.showerror('Ошибка', 'Заполните пустые поля')

    """
    Команда, осуществляющая запрос на удаление данных в таблицу БД.
    """

    def delete_record(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                employee_id = self._table.get_table().item(selection)['values'][0]
                date = self._table.get_table().item(selection)['values'][5]
                try:
                    answer = mb.askyesno('Подтверждение', 'Вы действительно хотите удалить выбранную запись?')
                    if answer:
                        CalculatedMonthWage.delete().where(
                            CalculatedMonthWage.employee_id == employee_id, CalculatedMonthWage.date == date).execute()
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
        parent.switch_frame(CalculatedMonthWagesFrame)
