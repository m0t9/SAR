colors = {
    1: 'color:#ff7b00',
    2: 'color:#ff0000;',
    0: 'color:#00ff00;',
    -1: 'color:#ff0000;'
}

adb_errors = {
    'linux2': 'в системе установлен пакет `adb` (sudo apt install adb).',
    'linux': 'в системе установлен пакет `adb` (sudo apt install adb).',
    'win32': 'установлены драйвера adb (DriverInstaller.msi) и в '
             'корневой папке SAR есть директория adb.'
}

removal_process_errors = {
    1: 'Не удалось удалить, похоже, что приложение уже отсутствует на устройстве',
    2: 'Не удалось удалить, похоже, что устройство не подключено, или на нем не включена отладка по USB',
    0: 'Приложение успешно удалено',
    -1: 'Произошла неизвестная ошибка, похоже, что удаление этого приложения недоступно'
}


def decode_error(code):
    return removal_process_errors[code]


def make_verdict(app_name, error):
    verdict = f'{app_name}: {decode_error(error)}'
    return f'<span style={colors[error]}>{verdict}</span>'
