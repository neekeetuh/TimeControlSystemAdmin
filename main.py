from interface.administrator import *

"""
Главная функция, внутри которой происходит вызов приложения для администрирования.
"""


def main():
    admin = AdministratorInterface()
    admin.start_app()


"""
Конструкция, запускающая главный скрипт.
"""
if __name__ == "__main__":
    main()
