from models.calculated_month_wage import *
from tkinter import messagebox as mb
from .Table import *

"""
Класс DepartmentsFrame является наследником tk.Frame, представляет собой экран, содержащий информацию об отделах с 
набором кнопок для определённых действий с записями таблицы.
"""


class DepartmentsFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self._table = Table(self, headings=['ID отдела', 'Адрес'], rows=self.get_data())
        self._table.pack()

        self._address_label = tk.Label(self, text='Адрес отдела:')
        self._entry_text = tk.StringVar()
        self._address_entry = tk.Entry(self, textvariable=self._entry_text)
        self._cancel_button = tk.Button(self, text='Отмена', command=self.cancel_action, background='lightblue')
        self._save_button = tk.Button(self, text='Сохранить', background='lightblue')

        self._insert_button = tk.Button(self, text='Добавить запись', command=self.insert_record_init,
                                        background='lightblue')
        self._update_button = tk.Button(self, text='Изменить запись', command=self.update_record_init,
                                        background='lightblue')
        self._delete_button = tk.Button(self, text='Удалить запись', command=self.delete_record, background='lightblue')
        self._insert_button.pack()
        self._update_button.pack()
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
            for department in Department.select().order_by(Department.id):
                content = [
                    department.id,
                    department.address,
                ]
                data.append(content)
        return data

    """
    Команда, отображающая форму для добавления записи в таблицу БД.
    """

    def insert_record_init(self):
        self._address_label.pack()
        self._address_entry.pack()
        self._cancel_button.pack()
        self._save_button.pack()
        self._save_button['command'] = self.insert_record
        self._delete_button['state'] = 'disabled'
        self._update_button['state'] = 'disabled'

    """
    Команда, отображающая форму для изменения определённой записи в таблице БД.
    """

    def update_record_init(self):
        if self._table.get_table().selection():
            self._delete_button['state'] = 'disabled'
            self._insert_button['state'] = 'disabled'
            for selection in self._table.get_table().selection():
                address = self._table.get_table().item(selection)['values'][1]
                self._address_label.pack()
                self._address_entry.pack()
                self._address_entry.delete(first=0, last=tk.END)
                self._address_entry.insert(0, address)
                self._cancel_button.pack()
                self._save_button.pack()
                self._save_button['command'] = self.update_record
        else:
            mb.showerror('Ошибка', 'Выберите запись для редактирования')

    """
    Команда, осуществляющая запрос на вставку данных в таблицу БД.
    """

    def insert_record(self):
        with db:
            if self._entry_text.get():
                Department.insert(address=self._entry_text.get()).execute()
                mb.showinfo('Успешно', 'Запись добавлена')
                self.refresh()
            else:
                mb.showerror('Ошибка', 'Заполните поле адрес')

    """
    Команда, осуществляющая запрос на изменение данных в таблицу БД.
    """

    def update_record(self):
        with db:
            if self._entry_text.get():
                for selection in self._table.get_table().selection():
                    record_id = self._table.get_table().item(selection)['values'][0]
                Department.update(address=self._entry_text.get()).where(Department.id == record_id).execute()
                mb.showinfo('Успешно', 'Запись изменена')
                self.refresh()
            else:
                mb.showerror('Ошибка', 'Заполните поле адрес')

    """
    Команда, осуществляющая запрос на удаление данных в таблицу БД.
    """

    def delete_record(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                record_id = self._table.get_table().item(selection)['values'][0]
                try:
                    answer = mb.askyesno('Подтверждение', 'Вы действительно хотите удалить выбранную запись?')
                    if answer:
                        Department.delete_by_id(record_id)
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
        parent.switch_frame(DepartmentsFrame)
