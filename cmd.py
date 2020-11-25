from os import system, chdir
from db_funcs import DatabaseTaker


def run(command):
    return system(command)


def remove_app(app_name, phone_model):
    dbt = DatabaseTaker()
    app_packet = dbt.get_packet_app(app_name, phone_model)
    if app_packet:
        chdir('adb')
        return run('adb shell pm uninstall -k --user 0 ' + app_packet)
    else:
        return 2

