from os import chdir
from subprocess import call, getstatusoutput
from sys import platform
from errors import adb_errors
import ctypes


def hide_shell():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_HIDE)


class CommandLine:
    # SET ON
    def __init__(self):
        self.error_message = str()
        try:
            chdir('adb')  # CHANGING DIRECTORY FOR WINDOWS
            call(['adb', 'start-server'])
        except Exception:  # IF ADB NOT FOUND
            self.error_message = f'Запуск программы невозможен, ' \
                                 f'убедитесь, что {adb_errors[platform]}'

    # KILL ADB SERVER ON EXIT
    def close_adb(self):
        try:
            call(['adb', 'kill-server'])
        except Exception:  # IF ADB NOT LAUNCHED
            pass

    # REMOVE SELECTED APP
    def remove_app(self, app_name, phone_model, dbt):
        is_connected = self.connection_check()
        if not is_connected:
            return 2

        app_packet = dbt.get_packet_app(app_name, phone_model)
        if app_packet:
            adb_ans = getstatusoutput(' '.join(['adb', 'shell', 'pm', 'uninstall', '-k', '--user 0', app_packet]))
            if adb_ans[1] == 'Failure [not installed for 0]':  # NO INSTALLED
                return 1
            elif adb_ans[1] == 'Failure [-1000]':  # NO ACCESS
                return -1
            elif adb_ans[1] == 'Success':  # SUCCESS
                return 0
            else:
                return 2  # NO CONNECTION OR ACCESS
        else:
            return 2

    # DEVICE CONNECTION CHECK
    def connection_check(self):
        output = getstatusoutput(' '.join(['adb', 'devices']))[1]
        if platform == 'linux' or platform == 'linux2':
            output = len(output.split('\n')) - 3
        elif platform == 'win32':
            output = len(output.split('\r\n')) - 3

        if output:
            return True
        return False
