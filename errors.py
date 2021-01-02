colors = {
    1: 'color:#ff7b00',
    2: 'color:#ff0000;',
    0: 'color:#00ff00;'
}


def decode_error(code):
    if code == 1:
        return 'Не удалось удалить, похоже, что приложение уже отсутствует на устройстве'
    elif code == 2:
        return 'Не удалось удалить, похоже, что устройство не подключено, или на нем не включена отладка по USB'
    elif code == 0:
        return 'Приложение успешно удалено'


def make_verdict(app_name, error):
    verdict = app_name + ': ' + decode_error(error)
    return '<span style=' + colors[error] + '>' + verdict + '</span>'
