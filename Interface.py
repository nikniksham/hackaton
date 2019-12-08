import sys
import sqlite3
from xlsxwriter.workbook import Workbook
from openpyxl import load_workbook
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class EntrepreneurDB:
    def __init__(self):
        self.location = 'test_db.db'


class Search(QWidget):
    def __init__(self):
        super().__init__()
        self.request = f'''SELECT * FROM Films
                                WHERE year >= 0'''
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
        self.Save_to_excel.clicked.connect(self.save_to_excel)

    def search(self):
        i = 0
        for name in self.test_characteristic:
            self.test_dictionary_characteristic[self.test_name_s[i]] = name.text()
            if name.text() == '':
                self.test_dictionary_characteristic[self.test_name_s[i]] = ''
            i += 1
        self.request = f'''SELECT * FROM Films
                        WHERE year >= 0'''
        for name in self.test_name_s:
            if self.test_dictionary_characteristic[name] != '':
                self.request += f''' and {name} like "%{self.test_dictionary_characteristic[name]}%"'''
        con = sqlite3.connect(self.db.location)
        cur = con.cursor()
        titles = cur.execute(self.request).description
        titles = [elem[0] for elem in titles]
        result = cur.execute(self.request).fetchall()
        con.close()
        self.table.setColumnCount(len(titles))
        self.table.setHorizontalHeaderLabels(titles)
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()

    def save_to_excel(self):
        workbook = Workbook('excel.xlsx')
        worksheet = workbook.add_worksheet()

        con = sqlite3.connect(self.db.location)
        cur = con.cursor()
        result = cur.execute(self.request).fetchall()
        con.close()
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                worksheet.write(i, j, row[j])
        workbook.close()


app = QApplication(sys.argv)
search = Search()
search.show()
sys.exit(app.exec_())