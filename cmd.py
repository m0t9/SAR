from os import system, chdir
from subprocess import check_output
from db_funcs import DatabaseTaker


# RUN CMD
def run(command):
    return system(command)


# REMOVE SELECTED APP
def remove_app(app_name, phone_model, dbt):
    try:
        app_packet = dbt.get_packet_app(app_name, phone_model)
        if app_packet:
            chdir('adb')
            return run('adb shell pm uninstall -k --user 0 ' + app_packet)
        else:
            return 2
    except:
        return 3


# DEVICE LIST
def device_connected():
    chdir('adb')
    output = (check_output('adb devices')).decode('utf-8')
    output = len(output.split('\r\n')) - 3

    if output:
        return True
    return False

