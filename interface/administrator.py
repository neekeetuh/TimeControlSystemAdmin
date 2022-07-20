import locale
import tkinter as tk

from interface.frames.CalculatedMonthWagesFrame import CalculatedMonthWagesFrame
from interface.frames.DataBaseFrame import DataBaseFrame
from interface.frames.DepartmentsFrame import DepartmentsFrame
from interface.frames.EmployeesFrame import EmployeesFrame
from interface.frames.PositionsFrame import PositionsFrame
from interface.frames.StandardWorkingCalendarFrame import StandardWorkingCalendarFrame
from interface.frames.WorkDaysFrame import WorkDaysFrame

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


class AdministratorInterface(tk.Tk):
    """
    Конструктор не принимает в себя никаких параметров и инициализирует в себе стандартные параметры библиотеки tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title("Администрирование TimeControlSystem")
        self.geometry("1920x1080")
        self.minsize(width=800, height=500)

        self._menu = tk.Menu(self)
        self.config(menu=self._menu)
        self._menu.add_command(label='База данных', command=lambda: self.switch_frame(DataBaseFrame))
        self._menu.add_command(label='Отделы', command=lambda: self.switch_frame(DepartmentsFrame))
        self._menu.add_command(label='Должности', command=lambda: self.switch_frame(PositionsFrame))
        self._menu.add_command(label='Сотрудники', command=lambda: self.switch_frame(EmployeesFrame))
        self._menu.add_command(label='Рабочие дни', command=lambda: self.switch_frame(WorkDaysFrame))
        self._menu.add_command(label='Расчёт зарплат',
                               command=lambda: self.switch_frame(CalculatedMonthWagesFrame))
        self._menu.add_command(label='Стандартный рабочий календарь',
                               command=lambda: self.switch_frame(StandardWorkingCalendarFrame))
        self._frame = None
        self.switch_frame(DataBaseFrame)

    """
    Функция, меняющая экраны. Параметр frame_class представляет собой класс экрана, который приложение должно 
    отобразить по команде.
    """

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    """
    Функция, запускающая клиентское приложение.
    """

    def start_app(self):
        self.mainloop()
