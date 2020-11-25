from os import system, chdir
from packets import packet_name


def run(command):
    return system(command)


def remove_app(app):
    chdir('adb')
    return run('adb shell pm uninstall -k --user 0 ' + packet_name[app])
