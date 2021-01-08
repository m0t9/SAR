import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from cmd import CommandLine
from db_funcs import DatabaseTaker
from errors import make_verdict


# REFERENCE WINDOW CLASS
class ReferenceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reference.ui', self)
        self.setWindowIcon(QIcon('res/icon.ico'))
        self.warning.setStyleSheet('color:red')


# MAIN WINDOW CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.setWindowIcon(QIcon('res/icon.ico'))

        self.reference_window = ReferenceWindow()

        self.dbt = DatabaseTaker()
        self.cmd = CommandLine()

        self.model.addItems(self.dbt.models_list)
        self.current_phone_model = self.dbt.models_list[0]

        self.compatible_apps = list()
        self.remove = list()

        self.model.currentIndexChanged.connect(self.load_compatible_apps)
        self.load_compatible_apps(0)

        self.apps.activated.connect(self.add_delete_app)
        self.remove_apps_button.setStyleSheet('color:red')
        self.remove_apps_button.clicked.connect(self.remove_selected_apps)

        self.reference.setStyleSheet('border:0')
        self.reference.clicked.connect(self.show_reference)

        self.clear_selected_button.clicked.connect(self.clear_selected)

    def load_compatible_apps(self, index):
        self.clear_selected()
        self.compatible_apps.clear()
        self.apps.clear()

        phone_model = self.dbt.models_list[index]
        self.current_phone_model = phone_model

        self.compatible_apps = self.dbt.get_phone_apps(phone_model)
        self.apps.addItems(self.compatible_apps)

    def add_delete_app(self, index):
        self.verdict_log.clear()
        self.verdict_log.setStyleSheet('color:#000000')
        self.clear_selected_button.setText('Очистить выбранное')

        application = self.compatible_apps[index]
        if application in self.remove:
            self.remove.pop(self.remove.index(application))
        else:
            self.remove.append(application)
        self.verdict_log.append('\n'.join(self.remove))

    def remove_selected_apps(self):
        full = len(self.remove)
        if full:
            if self.confirmation():
                self.removal_process()

    def show_reference(self):
        self.reference_window.show()

    def clear_selected(self):
        self.clear_selected_button.setText('Очистить выбранное')
        self.verdict_log.clear()
        self.remove.clear()
        self.verdict_log.setStyleSheet('color:#000000')

    def confirmation(self):
        answer = QMessageBox.question(self, 'Подтверждение', self.make_message(),
                                      QMessageBox.Yes,
                                      QMessageBox.No)
        if answer == QMessageBox.Yes:
            return True
        else:
            return False

    def make_message(self):
        text = 'Вы действительно хотите удалить '
        text += ', '.join(self.remove) + ' с Вашего устройства?'
        return text

    def removal_process(self):
        self.verdict_log.clear()
        for item in self.remove:
            verdict = make_verdict(item,
                                   self.cmd.remove_app(item, self.current_phone_model, self.dbt))
            self.verdict_log.append(verdict)
            self.verdict_log.append('<span></span>')
        self.remove.clear()
        self.clear_selected_button.setText('Очистить журнал')

    def closeEvent(self, event):
        self.reference_window.close()
        self.cmd.close_adb()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
