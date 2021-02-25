from PyQt5 import QtWidgets, QtCore, QtGui

import mainWindow
import sys
import os
import sqlite3


# def showDialog(self, dialog):
#     self.dialog = dialog(self)
#     self.dialog.show()

class FRaVGApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле mainWindow.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.Exit.triggered.connect(QtWidgets.qApp.quit)
        self.logoutAction.setDisabled(True)
        self.logoutAction.triggered.connect(self.logout_menus)
        self.authAction.triggered.connect(lambda: self.auth())
        self.UserRmv.triggered.connect(lambda: self.accounts('rmUser'))
        self.RemoveGuest.triggered.connect(lambda: self.accounts('rmGuest'))
        self.GuestAdd.triggered.connect(lambda: self.accounts('addGuest'))
        self.UserAdd.triggered.connect(lambda: self.accounts('addUser'))
        self.ModifyGuest.triggered.connect(lambda: self.accounts('modGuest'))
        self.UserModify.triggered.connect(lambda: self.accounts('modUser'))

    def unlock_menus(self, role):           # role - тип учетной записи (1 - Админ, 2 - обычный пользователь)
        if role == 1:
            self.GuestMenu.setEnabled(True)
            self.authAction.setDisabled(True)
            self.logoutAction.setEnabled(True)
        elif role == 2:
            self.GuestMenu.setEnabled(True)
            self.UsersMenu.setEnabled(True)
            self.authAction.setDisabled(True)
            self.logoutAction.setEnabled(True)

    def logout_menus(self):
        self.GuestMenu.setEnabled(False)
        self.UsersMenu.setEnabled(False)
        self.authAction.setEnabled(True)
        self.logoutAction.setEnabled(False)


    def auth(self):
        self.dialog = QtWidgets.QDialog(self)
        self.dialog.setWindowTitle('Авторизация')
        self.dialog.setModal(True)
        fbox = QtWidgets.QFormLayout()
        loginField = QtWidgets.QLineEdit()
        passField = QtWidgets.QLineEdit()
        passField.setEchoMode(QtWidgets.QLineEdit.Password)
        fbox.addRow('&Имя пользователя:', loginField)
        fbox.addRow('&Пароль:', passField)
        hbox = QtWidgets.QHBoxLayout()
        btnOK = QtWidgets.QPushButton('&OK')
        btnCancel = QtWidgets.QPushButton('&Отмена')
        hbox.addWidget(btnOK)
        hbox.addWidget(btnCancel)
        fbox.addRow(hbox)
        self.dialog.setLayout(fbox)
        btnCancel.clicked.connect(self.dialog.close)
        btnOK.clicked.connect(lambda: self.isValid(loginField.text(), passField.text()))
        self.dialog.adjustSize()
        self.dialog.show()
        self.dialog.exec_()

    def accounts(self, title):     # @TODO прикрутить функционал, кнопки, добавить чек бокс для rmUser чтобы не удалять гостевой профиль
        self.accWindow = QtWidgets.QDialog(self)
        self.accWindow.setModal(True)
        # self.prio = 1
        print(title)
        fbox = QtWidgets.QFormLayout()
        # self.photoView = QtWidgets.QGraphicsView()          # возможно надо удалить этот self вначале       self.photoView = QtWidgets.QGraphicsView() self.photoView = QtGui.QPixmap()
        # self.photoView.setContentsMargins(50, -1, 50, -1)
        self.photoLbl = QtWidgets.QLabel(self)
        self.photoView = QtGui.QPixmap("A_Fishful_of_Dollars.jpg")
        self.photoView.scaled(150, 200)
        self.photoLbl.setPixmap(self.photoView)
        fbox.addRow(self.photoLbl)
        self.fPath = QtWidgets.QLineEdit()
        self.fPath.setText('Укажите путь к файлу')
        self.fPath.setDragEnabled(True)
        self.btnBrowse = QtWidgets.QPushButton('&Обзор')
        self.btnDirBrowse = QtWidgets.QPushButton('&Фото')
        # btnBrowse.setFixedWidth(45)
        hPath = QtWidgets.QHBoxLayout()
        hPath.addWidget(self.fPath)
        hPath.addWidget(self.btnBrowse)
        hPath.addWidget(self.btnDirBrowse)
        fbox.addRow(hPath)
        ubox = QtWidgets.QFormLayout()
        loginField = QtWidgets.QLineEdit()
        passField = QtWidgets.QLineEdit()
        passField.setEchoMode(QtWidgets.QLineEdit.Password)
        extraBox = QtWidgets.QHBoxLayout()
        prioLbl = QtWidgets.QLineEdit('&Приоритет:')
        isAdmin = QtWidgets.QCheckBox('&Администратор', self)
        prioBox = QtWidgets.QComboBox()  # Приоритет приветствия
        prioBox.addItems(['1-обычный', '2-Высокий', '3-Первоочередной'])        # @TODO Исправить
        extraBox.addWidget(prioBox)
        # prio = 1
        # print(prio)

        # def set_priority():
        #     prio = prioBox.currentIndex()
        #     print(prio)

        # prioBox.activated.connect(set_priority)
        if title == 'rmUser':
            self.accWindow.setWindowTitle('Удаление учетной записи пользователя')
        elif title == 'addGuest':
            self.accWindow.setWindowTitle('Добавить гостя')
            fbox.addRow(extraBox)
        elif title == 'addUser':
            self.accWindow.setWindowTitle('Создание учетной записи пользователя')
            ubox.addRow('&Имя пользователя:', loginField)
            ubox.addRow('&Пароль:', passField)
            fbox.addRow(ubox)
            extraBox.addWidget(isAdmin)
            fbox.addRow(extraBox)
        elif title == 'modGuest':
            self.accWindow.setWindowTitle('Изменение данных гостя')
            fbox.addRow(extraBox)
        elif title == 'modUser':
            self.accWindow.setWindowTitle('Изменение учетной записи пользователя')
            ubox.addRow('&Пароль:', passField)
            fbox.addRow(ubox)
            extraBox.addWidget(isAdmin)
            fbox.addRow(extraBox)

        else:
            self.accWindow.setWindowTitle('Удаление данных гостя')

        self.fName = QtWidgets.QLineEdit()
        self.fLastName = QtWidgets.QLineEdit()
        self.fSecondName = QtWidgets.QLineEdit()
        fbox.addRow('&Фамилия:', self.fLastName)
        fbox.addRow('&Имя:', self.fName)
        fbox.addRow('&Отчество:', self.fSecondName)
        # fbox.addRow('Приоритет', self.prio)
        hbtn = QtWidgets.QHBoxLayout()
        btnFnd = QtWidgets.QPushButton('&Найти')
        btnOK = QtWidgets.QPushButton('&OK')
        btnCancel = QtWidgets.QPushButton('&Cancel')
        hbtn.addWidget(btnFnd)
        hbtn.addWidget(btnOK)
        hbtn.addWidget(btnCancel)
        fbox.addRow(hbtn)
        btnCancel.clicked.connect(self.accWindow.close)
        self.btnBrowse.clicked.connect(self.browse_file)
        # btnOK.clicked.connect(сохраняем фото в папку /known , проверяем наличие логина, если нет то добавляем данные в БД)
        self.accWindow.setLayout(fbox)
        self.accWindow.adjustSize()
        self.accWindow.show()
        self.accWindow.exec_()

    #  @TODO: Довести до ума функцию isValid(), добавить поиск login'a в БД и затем сверку пароля
    def isValid(self, log, passw):
            print(log + " & " + passw)          # remove me!
            #   Должно быть:
            #   1. Поиск в БД Логин
            #   2. сравнение паролей > если не верно сообщить об ошибке
            #   3. если верно получить из БД: id, ФИО, приоритет, админ или нет, вывести фото в виджет
            prio = 1
            if log == 'login1' and passw == 'password1':
                prio = 2
                self.unlock_menus(prio)
                self.dialog.close()
            elif log == 'login2' and passw == 'password2':
                self.unlock_menus(prio)
                self.dialog.close()
            else:
                pop = QtWidgets.QMessageBox()
                pop.setWindowTitle('Ошибка авторизации!')
                pop.setText('Неверные имя пользователя или пароль')
                pop.adjustSize()
                pop.show()
                pop.exec_()

    def browse_folder(self):
        self.listWidget             # temp item
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose directory")        #temp item

        if directory:                                           # temp item
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)

    def browse_file(self):
        self.fPath
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", '/home')[0]
        self.fPath.setText(fname)
        self.photoView.load(str(fname))
        self.photoView.scaled(150, 200)
        self.photoLbl.setPixmap(self.photoView)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = FRaVGApp()  # Создаём объект класса FRaVGApp

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()