import tkinter as tk
import tkinter.ttk as ttk

"""
Класс Table является наследником tk.Frame, представляет собой таблицу для отображения данных из БД.
"""


class Table(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры. Параметр parent представляет собой экземпляр стандартного
    объекта tkinter, к которому будет привязана таблица. Параметр headings представляет собой коллекцию из заголовков
    таблицы. Параметр rows представляет собой коллекцию из строк таблицы.
    """

    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        self._table = ttk.Treeview(self, show="headings", selectmode="browse")
        self._table["columns"] = headings
        self._table["displaycolumns"] = headings

        for head in headings:
            self._table.heading(head, text=head, anchor=tk.CENTER)
            self._table.column(head, anchor=tk.CENTER)

        for row in rows:
            self._table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=self._table.yview)
        self._table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self._table.pack(expand=tk.YES, fill=tk.BOTH)

    """
    Функция, возвращающая таблицу и обеспечивающая доступ к ней.
    """

    def get_table(self):
        return self._table
