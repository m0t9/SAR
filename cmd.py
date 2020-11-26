from os import system, chdir
from subprocess import check_output
from db_funcs import DatabaseTaker


class CommandLine:
    # SET ON
    def __init__(self):
        chdir('adb')

    # RUN CMD
    @staticmethod
    def run(command):
        return system(command)

    # REMOVE SELECTED APP
    @staticmethod
    def remove_app(app_name, phone_model, dbt):
        try:
            app_packet = dbt.get_packet_app(app_name, phone_model)
            if app_packet:
                return run('adb shell pm uninstall -k --user 0 ' + app_packet)
            else:
                return 2
        except:
            return 3

    # DEVICE CONNECTION CHECK
    @staticmethod
    def connection_check(self):
        output = (check_output('adb devices')).decode('utf-8')
        output = len(output.split('\r\n')) - 3

        if output:
            return True
        return False
