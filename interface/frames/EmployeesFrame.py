from models.calculated_month_wage import *
from tkinter import messagebox as mb
from .Table import *

"""
Класс EmployeesFrame является наследником tk.Frame, представляет собой экран, содержащий информацию о сотрудниках с 
набором кнопок для определённых действий с записями таблицы.
"""


class EmployeesFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        headings = ['ID сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Электронная почта', 'Номер телефона', 'Должность',
                    'Отдел']
        self._table = Table(self, headings=headings, rows=self.get_data())
        self._table.pack()

        self._surname_label = tk.Label(self, text='Фамилия*:')
        self._entry_text_surname = tk.StringVar()
        self._surname_entry = tk.Entry(self, textvariable=self._entry_text_surname)

        self._name_label = tk.Label(self, text='Имя*:')
        self._entry_text_name = tk.StringVar()
        self._name_entry = tk.Entry(self, textvariable=self._entry_text_name)

        self._patronymic_label = tk.Label(self, text='Отчество:')
        self._entry_text_patronymic = tk.StringVar()
        self._patronymic_entry = tk.Entry(self, textvariable=self._entry_text_patronymic)

        self._email_label = tk.Label(self, text='Электронная почта:')
        self._entry_text_email = tk.StringVar()
        self._email_entry = tk.Entry(self, textvariable=self._entry_text_email)

        self._phone_number_label = tk.Label(self, text='Номер телефона (без +)*:')
        self._entry_text_phone_number = tk.StringVar()
        self._phone_number_entry = tk.Entry(self, textvariable=self._entry_text_phone_number)

        self._position_label = tk.Label(self, text='Должность*:')
        position_values = []
        with db:
            for position in Position.select():
                position_values.append(position.title)
        self._position_entry = ttk.Combobox(self, values=position_values)

        self._department_label = tk.Label(self, text='Отдел*:')
        department_values = []
        with db:
            for department in Department.select():
                department_values.append(department.address)
        self._department_entry = ttk.Combobox(self, values=department_values)

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
            for employee in Employee.select().order_by(Employee.id):
                content = [
                    employee.id,
                    employee.surname,
                    employee.name,
                    employee.patronymic,
                    employee.email,
                    employee.phone_number,
                    employee.position_id.title,
                    employee.department_id.address
                ]
                data.append(content)
        return data

    """
    Команда, отображающая форму для добавления записи в таблицу БД.
    """

    def insert_record_init(self):
        self._surname_label.pack()
        self._surname_entry.pack()
        self._name_label.pack()
        self._name_entry.pack()
        self._patronymic_label.pack()
        self._patronymic_entry.pack()
        self._email_label.pack()
        self._email_entry.pack()
        self._phone_number_label.pack()
        self._phone_number_entry.pack()
        self._position_label.pack()
        self._position_entry.pack()
        self._department_label.pack()
        self._department_entry.pack()
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
                surname, name, patronymic, email, phone_number, position_title, department_address = \
                    self._table.get_table().item(selection)['values'][1:8]
                self._surname_label.pack()
                self._surname_entry.pack()
                self._surname_entry.delete(first=0, last=tk.END)
                self._surname_entry.insert(0, surname)

                self._name_label.pack()
                self._name_entry.pack()
                self._name_entry.delete(first=0, last=tk.END)
                self._name_entry.insert(0, name)

                self._patronymic_label.pack()
                self._patronymic_entry.pack()
                self._patronymic_entry.delete(first=0, last=tk.END)
                self._patronymic_entry.insert(0, patronymic)

                self._email_label.pack()
                self._email_entry.pack()
                self._email_entry.delete(first=0, last=tk.END)
                self._email_entry.insert(0, email)

                self._phone_number_label.pack()
                self._phone_number_entry.pack()
                self._phone_number_entry.delete(first=0, last=tk.END)
                self._phone_number_entry.insert(0, phone_number)

                self._position_label.pack()
                self._position_entry.set(position_title)
                self._position_entry.pack()

                self._department_label.pack()
                self._department_entry.set(department_address)
                self._department_entry.pack()

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
            if self._entry_text_surname.get() and self._entry_text_name.get() and self._entry_text_phone_number.get() \
                    and self._position_entry.get() and self._department_entry.get():
                Employee.insert(surname=self._entry_text_surname.get(),
                                name=self._entry_text_name.get(),
                                patronymic=self._entry_text_patronymic.get(),
                                email=self._entry_text_email.get(),
                                phone_number=self._entry_text_phone_number.get(),
                                position_id=Position.get(Position.title == self._position_entry.get()).id,
                                department_id=Department.get(Department.address == self._department_entry.get()).id
                                ).execute()
                mb.showinfo('Успешно', 'Запись добавлена')
                self.refresh()
            else:
                mb.showerror('Ошибка', 'Заполните обязательные поля, помеченные *')

    """
    Команда, осуществляющая запрос на изменение данных в таблицу БД.
    """

    def update_record(self):
        with db:
            if self._entry_text_surname.get() and self._entry_text_name.get() and self._entry_text_phone_number.get() \
                    and self._position_entry.get() and self._department_entry.get():
                for selection in self._table.get_table().selection():
                    employee_id = self._table.get_table().item(selection)['values'][0]
                Employee.update(surname=self._entry_text_surname.get(),
                                name=self._entry_text_name.get(),
                                patronymic=self._entry_text_patronymic.get(),
                                email=self._entry_text_email.get(),
                                phone_number=self._entry_text_phone_number.get(),
                                position_id=Position.get(Position.title == self._position_entry.get()).id,
                                department_id=Department.get(Department.address == self._department_entry.get()).id
                                ).where(
                    Employee.id == employee_id).execute()
                mb.showinfo('Успешно', 'Запись изменена')
                self.refresh()
            else:
                mb.showerror('Ошибка', 'Заполните обязательные поля, помеченные *')

    """
    Команда, осуществляющая запрос на удаление данных в таблицу БД.
    """

    def delete_record(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                employee_id = self._table.get_table().item(selection)['values'][0]
                try:
                    answer = mb.askyesno('Подтверждение', 'Вы действительно хотите удалить выбранную запись?')
                    if answer:
                        Employee.delete_by_id(employee_id)
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
        parent.switch_frame(EmployeesFrame)
