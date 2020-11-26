def decode_error(code):
    if code == 1:
        return 'Не удалось удалить, похоже, что приложение отсутствует на устройстве'
    elif code == 3:
        return 'Не удалось удалить, похоже, что устройство не подключено, или на нем не включена отладка по USB'
    elif code == 0:
        return 'Приложение успешно удалено'

def make_verdict(app_name, error):
    verdict = app_name + ': ' + decode_error(error)
    return verdict