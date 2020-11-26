import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui, QtCore, QtWidgets, Qt
from cmd import remove_app, run
from db_funcs import DatabaseTaker
from errors import decode_error


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)

        self.dbt = DatabaseTaker()
        self.model.addItems(self.dbt.models_list)
        self.current_phone_model = self.dbt.models_list[0]

        self.compatible_apps = list()
        self.remove = list()

        self.model.currentIndexChanged.connect(self.load_compatible_apps)
        self.load_compatible_apps(0)

        self.apps.activated.connect(self.add_delete_app)
        self.remove_apps_button.clicked.connect(self.remove_choosed_apps)

    def load_compatible_apps(self, index):
        self.remove.clear()
        self.progress_log.clear()
        self.compatible_apps.clear()
        self.apps.clear()
        phone_model = self.dbt.models_list[index]
        self.current_phone_model = phone_model
        self.compatible_apps = self.dbt.get_phone_apps(phone_model)
        self.apps.addItems(self.compatible_apps)

    def add_delete_app(self, index):
        self.progress_log.clear()
        application = self.compatible_apps[index]
        if application in self.remove:
            self.remove.pop(self.remove.index(application))
        else:
            self.remove.append(application)
        self.progress_log.setPlainText('\n'.join(self.remove))

    def remove_choosed_apps(self):
        self.progress_log.clear()
        result = list()
        for item in self.remove:
            verdict = item + ': ' + decode_error(remove_app(item, self.current_phone_model, self.dbt))
            result.append(verdict)
        self.progress_log.appendPlainText('\n\n'.join(result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
