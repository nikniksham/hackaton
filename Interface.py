import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class EntrepreneurDB:
    def __init__(self):
        self.location = 'test_db.db'


class Search(QWidget):
    def __init__(self):
        super().__init__()
        self.db = EntrepreneurDB()
        uic.loadUi('Interface_program.ui', self)
        self.characteristic = [self.surname, self.name, self.patronymic, self.name_company, self.INN, self.OGRN,
                               self.mail, self.phone, self.social_network, self.site, self.human_settlement,
                               self.victory_in_procurement, self.Participation_in_procurement, self.Getting_support]
        self.name_s = ['Фамилия', 'Имя', 'Отчество', 'Название компании', 'ИНН', 'ОГРН', 'Почта', 'Телефон',
                       'Социальные сети', 'Сайт', 'Населённый пункт', 'Победы в закупках', 'Участие в закупках',
                       'Получение поддержки']
        self.dictionary_characteristic = {'Фамилия': '', 'Имя': '', 'Отчество': '', 'Название компании': '', 'ИНН': '',
                                          'ОГРН': '', 'Почта': '', 'Телефон': '', 'Социальные сети': '', 'Сайт': '',
                                          'Населённый пункт': '', 'Победы в закупках': '', 'Участие в закупках': '',
                                          'Получение поддержки': ''}
        self.test_name_s = ['id', 'title', 'year', 'genre', 'duration']
        self.test_characteristic = [self.surname, self.name, self.patronymic, self.name_company, self.INN]
        self.test_dictionary_characteristic = {'id': '', 'title': '', 'year': '', 'genre': '', 'duration': ''}
        self.Search.clicked.connect(self.search)

    def search(self):
        # создаём запрос
        i = 0
        for name in self.test_characteristic:
            self.test_dictionary_characteristic[self.test_name_s[i]] = name.text()
            if name.text() == '':
                self.test_dictionary_characteristic[self.test_name_s[i]] = ''
            i += 1
        request = f'''SELECT * FROM Films
                        WHERE year >= 0'''
        for name in self.test_name_s:
            if self.test_dictionary_characteristic[name] != '':
                request += f''' and {name} like "%{self.test_dictionary_characteristic[name]}%"'''
        # Подключение к БД
        con = sqlite3.connect(self.db.location)
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        titles = cur.execute(request).description
        titles = [elem[0] for elem in titles]
        result = cur.execute(request).fetchall()
        # закрываем базу данных
        con.close()
        # задаём ширину таблицы
        self.table.setColumnCount(len(titles))
        # задаём заголовки столбцов
        self.table.setHorizontalHeaderLabels(titles)
        # задаём количество строк
        self.table.setRowCount(len(result))
        # задаём значения строкам
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()


app = QApplication(sys.argv)
search = Search()
search.show()
sys.exit(app.exec_())