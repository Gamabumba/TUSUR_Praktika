from tkinter import ttk
import tkinter as tk
import psycopg2
from psycopg2 import Error
from db_operations import delete_from_db
from collect_data import collect_data


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.see_db()

    def init_main(self):
        toolbar = tk.Frame(bg='#F0E68C', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Обновить базу данных', command=self.open_dialog, bg='#F0E68C', bd=0, compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Имя предприятия', 'Ссылка', 'Должность руководителя', 'ФИО руководителя',
                                                'Телефоны', 'Email', 'Адрес', 'Сайт', 'Дата основания',
                                                'Об организации', 'Дата обновления оинформации'), height=35, show='headings')
        self.tree.column('ID', width=20, anchor=tk.CENTER)
        self.tree.column('Имя предприятия', width=150, anchor=tk.CENTER)
        self.tree.column('Ссылка', width=80, anchor=tk.CENTER)
        self.tree.column('Должность руководителя', width=80, anchor=tk.CENTER)
        self.tree.column('ФИО руководителя', width=80, anchor=tk.CENTER)
        self.tree.column('Телефоны', width=80, anchor=tk.CENTER)
        self.tree.column('Email', width=200, anchor=tk.CENTER)
        self.tree.column('Адрес', width=200, anchor=tk.CENTER)
        self.tree.column('Сайт', width=150, anchor=tk.CENTER)
        self.tree.column('Дата основания', width=100, anchor=tk.CENTER)
        self.tree.column('Об организации', width=100, anchor=tk.CENTER)
        self.tree.column('Дата обновления оинформации', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Имя предприятия', text='Имя предприятия')
        self.tree.heading('Ссылка', text='Ссылка')
        self.tree.heading('Должность руководителя', text='Должность руководителя')
        self.tree.heading('ФИО руководителя', text='ФИО руководителя')
        self.tree.heading('Телефоны', text='Телефоны')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Адрес', text='Адрес')
        self.tree.heading('Сайт', text='Сайт')
        self.tree.heading('Дата основания', text='Дата основания')
        self.tree.heading('Об организации', text='Об организации')
        self.tree.heading('Дата обновления оинформации', text='Дата обновления оинформации')

        self.tree.pack(side=tk.LEFT)

        scroll_y = tk.Scrollbar(self, command=self.tree.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)

        scroll_x = tk.Scrollbar(self, command=self.tree.xview)
        scroll_x.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(xscrollcommand=scroll_x.set)

    def see_db(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        try:

            connection = psycopg2.connect(user="postgres",
                                          password="cfnjyby2002",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="partners_db")

            with connection.cursor() as cursor:
                cursor.execute("Select * From partners")
                rows = cursor.fetchall()
                [self.tree.insert('', 'end', values=row) for row in rows]

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

        finally:
            if connection:
                connection.close()

    def open_dialog(self):
        UpdateWindow()


class UpdateWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_update()

    def main(self):
        delete_from_db()
        collect_data()
        self.destroy()

    def init_update(self):
        self.title("Вы уверены?")
        self.geometry('250x170+400+300')
        self.resizable(False, False)

        btn_cancel = ttk.Button(self, text='Нет', command=self.destroy)
        btn_accept = ttk.Button(self, text='Да', command=self.main)

        btn_cancel.place(x=150, y=85)
        btn_accept.place(x=50, y=85)

        self.grab_set()
        self.focus_set()

