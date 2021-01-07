from os import chdir
from subprocess import check_output, CalledProcessError, call
from sys import platform


class CommandLine:
    # SET ON
    def __init__(self):
        chdir('adb')  # CHANGING DIRECTORY FOR WINDOWS
        call(['adb', 'start-server'])

    # REMOVE SELECTED APP
    def remove_app(self, app_name, phone_model, dbt):
        is_connected = self.connection_check()
        if not is_connected:
            return 2
        try:
            app_packet = dbt.get_packet_app(app_name, phone_model)
            if app_packet:
                return call(['adb', 'shell', 'pm', 'uninstall', '-k', '--user 0', app_packet])
            else:
                return 2
        except CalledProcessError:
            return 2

    # DEVICE CONNECTION CHECK
    def connection_check(self):
        output = (check_output(['adb', 'devices'])).decode('utf-8')

        if platform == 'linux' or platform == 'linux2':
            output = len(output.split('\n')) - 3
        elif platform == 'win32':
            output = len(output.split('\r\n')) - 3

        if output:
            return True
        return False
