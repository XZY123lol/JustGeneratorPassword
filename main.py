import sys
import os
import secrets
import string
import pyperclip
from PyQt5 import QtWidgets, QtGui
from ui_main import Ui_MainWindow

class PasswordGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        icon_path = os.path.join("assets", "icon.ico")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowTitle("JustGeneratorPassword")
        self.setFixedSize(800, 600)

        self.ui.pushButton.clicked.connect(self.generate_password)
        self.ui.pushButton_2.clicked.connect(self.copy_password)
        self.ui.checkBox.stateChanged.connect(self.update_password_visibility)

        self.current_password = ''
    
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

    def generate_password(self):
        length = self.ui.spinBox.value()
        use_symbols = self.ui.checkBox_2.isChecked()
        use_digits = self.ui.checkBox_3.isChecked()
        use_letters = self.ui.checkBox_4.isChecked()

        pool = ''
        if use_letters:
            pool += string.ascii_letters
        if use_digits:
            pool += string.digits
        if use_symbols:
            pool += string.punctuation

        if not pool:
            self.ui.statusbar.showMessage("Выберите хотя бы один тип символов!", 3000)
            return

        password = ''.join(secrets.choice(pool) for _ in range(length))
        self.current_password = password

        if self.ui.checkBox.isChecked():
            self.ui.textEdit.setPlainText(password)
        else:
            self.ui.textEdit.setPlainText('*' * len(password))

        self.ui.statusbar.showMessage("Пароль сгенерирован", 3000)

    def copy_password(self):
        if self.current_password:
            pyperclip.copy(self.current_password)
            self.ui.statusbar.showMessage("Пароль скопирован", 3000)
        else:
            self.ui.statusbar.showMessage("Нет пароля для копирования", 3000)

    def update_password_visibility(self):
        if self.current_password:
            if self.ui.checkBox.isChecked():
                self.ui.textEdit.setPlainText(self.current_password)
            else:
                self.ui.textEdit.setPlainText('*' * len(self.current_password))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())