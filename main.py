import sys

from cmd import CommandLine, hide_shell
from db_funcs import DatabaseTaker
from errors import make_verdict, colors

if sys.platform == 'win32':  # HIDE SHELL WINDOW (ONLY WIN32)
    hide_shell()

from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFrame


# SIGNAL FOR PROGRESS BAR
class ProgressBarSignal(QObject):
    valueUpdated = pyqtSignal(int)


'''
# REFERENCE WINDOW CLASS
class ReferenceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reference.ui', self)
        self.setWindowIcon(QIcon('res/icon.ico'))
        self.warning.setStyleSheet(colors["fail"])
        self.resize_widgets()

    def resize_widgets(self):
        resized_font = self.font()

        resized_font.setPointSize(13)
        self.label.setFont(resized_font)

        resized_font.setPointSize(11)
        for widget in [self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.warning]:
            widget.setFont(resized_font)
'''


# MAIN WINDOW CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.setWindowIcon(QIcon('res/icon.ico'))
        self.resize_widgets()

        # ASSEMBLING REFERENCE
        # self.reference_window = ReferenceWindow()

        # self.reference.clicked.connect(self.show_reference)

        # ASSEMBLING COMMAND LINE AND DATABASE TAKER
        self.dbt = DatabaseTaker()
        self.cmd = CommandLine()

        if self.cmd.error_message:
            self.verdict_log.append(self.cmd.error_message)
        else:
            # CHECKING DB STATUS
            if self.dbt.newest_db:
                self.database_status.setText('Подключена новейшая база данных')
                self.database_status.setStyleSheet(colors['success'])
            else:
                self.database_status.setText('Подключена устаревшая база данных')
                self.database_status.setStyleSheet(colors['fail'])

            # LOADING PHONE MODELS AND COMPATIBLE APPS
            self.model.addItems(self.dbt.models_list)
            self.current_phone_model = self.dbt.models_list[0]
            self.verdict_log.setFrameStyle(QFrame.NoFrame)

            self.compatible_apps = list()
            self.remove = list()

            self.model.currentIndexChanged.connect(self.load_compatible_apps)
            self.load_compatible_apps(0)

            self.apps.activated.connect(self.add_delete_app)
            self.remove_apps_button.clicked.connect(self.remove_selected_apps)

            self.clear_selected_button.clicked.connect(self.clear_selected)

            # ASSEMBLING PROGRESS BAR SIGNAL
            self.pb_signal = ProgressBarSignal(self)
            self.pb_signal.valueUpdated.connect(self.update_pb)

            self.current_load = 0
            self.target_load = 0

    def load_compatible_apps(self, index):
        self.clear_selected()
        self.compatible_apps.clear()
        self.apps.clear()

        phone_model = self.dbt.models_list[index]
        self.current_phone_model = phone_model

        self.compatible_apps = self.dbt.get_phone_apps(phone_model)
        self.apps.addItems(self.compatible_apps)

    def add_delete_app(self, index):
        self.current_load = 0
        self.target_load = 0
        self.update_pb()

        self.verdict_log.clear()
        self.verdict_log.setStyleSheet(colors['default'])
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
            self.target_load = full
            if self.confirmation():
                self.removal_process()

    '''
    def show_reference(self):
        self.reference_window.show()
    '''

    def clear_selected(self):
        self.current_load = 0
        self.target_load = 0
        self.update_pb()

        self.clear_selected_button.setText('Очистить выбранное')

        self.verdict_log.clear()
        self.remove.clear()
        self.verdict_log.setStyleSheet(colors['default'])

    def confirmation(self):
        answer = QMessageBox(self)
        answer.setIcon(QMessageBox.Warning)
        answer.setWindowTitle('Подтвердите удаление')
        answer.setText(self.make_message())

        accept = answer.addButton('Да', QMessageBox.AcceptRole)
        reject = answer.addButton('Нет', QMessageBox.RejectRole)

        answer.setDefaultButton(accept)

        accept.setStyleSheet('''QPushButton {
                                border: solid gray;
                                font-weight: bold;
                                color: red;
                                font-size: 20px;
                                padding-top: 5px;
                                padding-bottom: 5px;
                                padding-left: 20px;
                                padding-right: 20px;
                                border-radius: 10;
                                background-color: #dedede;
                                }
                                QPushButton:hover {
                                    background-color: #cccccc;
                                }
                            
                                QPushButton:pressed {
                                    background-color: #c4c4c4;
                                }''')
        reject.setStyleSheet('''QPushButton {
                                border: solid gray;
                                border-radius: 10;
                                padding-top: 5px;
                                padding-bottom: 5px;
                                padding-left: 20px;
                                padding-right: 20px;
                                font-size: 20px;
                                background-color: #dedede;
                                }
                                QPushButton:hover {
                                    background-color: #cccccc;
                                }

                                QPushButton:pressed {
                                    background-color: #c4c4c4;
                                }''')

        answer.exec()
        answer.deleteLater()

        if answer.clickedButton() is accept:
            return True
        else:
            return False

    def make_message(self):
        applications = ', '.join(self.remove)
        text = f'Вы действительно хотите удалить {applications} с Вашего устройства?'
        return text

    def removal_process(self):
        self.verdict_log.clear()
        for item in self.remove:
            verdict = make_verdict(item,
                                   self.cmd.remove_app(item, self.current_phone_model, self.dbt))
            self.verdict_log.append(verdict)
            self.verdict_log.append('<span></span>')

            self.current_load += 1
            self.pb_signal.valueUpdated.emit(1)
        self.remove.clear()
        self.clear_selected_button.setText('Очистить журнал')

    def closeEvent(self, event):
        # self.reference_window.close()
        try:
            self.cmd.close_adb()
        except Exception as exc:
            pass

    def update_pb(self):
        if not self.current_load:
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setValue(int(100 * self.current_load / self.target_load))

    # FUNCTION FOR RESIZE WIDGETS
    def resize_widgets(self):
        resized_font = self.font()

        resized_font.setPointSize(11)
        for widget in [self.database_status, self.model_label, self.apps_label]:
            widget.setFont(resized_font)

        resized_font.setPointSize(8)
        self.clear_selected_button.setFont(resized_font)

        resized_font.setPointSize(7)
        self.model.setFont(resized_font)
        self.apps.setFont(resized_font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
