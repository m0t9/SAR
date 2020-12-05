import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from cmd import CommandLine
from db_funcs import DatabaseTaker
from errors import decode_error, make_verdict


class ReferenceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reference.ui', self)

        self.warning.setStyleSheet('color:red')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)

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
        self.progress_log.clear()
        application = self.compatible_apps[index]
        if application in self.remove:
            self.remove.pop(self.remove.index(application))
        else:
            self.remove.append(application)
        self.progress_log.setPlainText('\n'.join(self.remove))

    def remove_selected_apps(self):
        self.progress_log.clear()

        full = len(self.remove)
        if full:
            for item in self.remove:
                verdict = make_verdict(item,
                                       self.cmd.remove_app(item, self.current_phone_model, self.dbt))
                self.progress_log.appendPlainText(verdict + '\n')
            self.remove.clear()

    def show_reference(self):
        self.reference_window.show()

    def clear_selected(self):
        self.remove.clear()
        self.progress_log.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
