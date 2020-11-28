import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui, QtCore, QtWidgets, Qt
from cmd import CommandLine
from db_funcs import DatabaseTaker
from errors import decode_error, make_verdict


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)

        self.dbt = DatabaseTaker()
        self.cmd = CommandLine()

        self.model.addItems(self.dbt.models_list)
        self.current_phone_model = self.dbt.models_list[0]

        self.compatible_apps = list()
        self.remove = list()

        self.model.currentIndexChanged.connect(self.load_compatible_apps)
        self.load_compatible_apps(0)

        self.apps.activated.connect(self.add_delete_app)
        self.remove_apps_button.clicked.connect(self.remove_choosed_apps)


    def load_compatible_apps(self, index):
        self.progress_bar.setValue(0)
        self.remove.clear()
        self.progress_log.clear()
        self.compatible_apps.clear()
        self.apps.clear()

        phone_model = self.dbt.models_list[index]
        self.current_phone_model = phone_model

        self.compatible_apps = self.dbt.get_phone_apps(phone_model)
        self.apps.addItems(self.compatible_apps)

    def add_delete_app(self, index):
        self.progress_bar.setValue(0)
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

        full = len(self.remove)
        current = 0

        if full:
            self.progress_bar.setValue(current // full * 100)
            for item in self.remove:
                verdict = make_verdict(item,
                                       self.cmd.remove_app(item, self.current_phone_model, self.dbt))
                result.append(verdict)
                current += 1
                self.progress_bar.setValue(current // full * 100)

            self.progress_log.appendPlainText('\n\n'.join(result))
            self.remove.clear()
            result.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
