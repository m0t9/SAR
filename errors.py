colors = {
    'default': 'color:#000000;',
    'success': 'color:#00BB3F;',
    'not success': 'color:#ff7b00;',
    'fail': 'color:#ff0000;'
}

adb_errors = {
    'linux2': 'в системе установлен пакет `adb` (sudo apt install adb).',
    'linux': 'в системе установлен пакет `adb` (sudo apt install adb).',
    'win32': 'установлены драйвера adb (DriverInstaller.msi) и в '
             'корневой папке SAR есть директория adb.'
}

removal_process_errors = {
    1: ('Не получилось удалить, похоже, что приложение уже отсутствует на устройстве', 'not success'),
    2: ('Не получилось удалить, похоже, что устройство не подключено, или на нем не включена отладка по USB', 'fail'),
    0: ('Приложение успешно удалено', 'success'),
    -1: ('Произошла неизвестная ошибка, похоже, что удаление этого приложения недоступно', 'fail')
}


def decode_error(code):
    return removal_process_errors[code]


def make_verdict(app_name, error_code):
    message, error_type = decode_error(error_code)
    verdict = f'{app_name}: {message}'
    return f'<span style={colors[error_type]}>{verdict}</span>'
