from os import system

from packets import packet_name


def run(command):
    system(command)


def remove_app(app):
    run('cd adb')
    run('adb shell pm uninstall -k --user 0' + packet_name[app])
