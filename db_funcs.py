from sqlite3 import connect, OperationalError


class DatabaseTaker:
    def __init__(self):
        self.db = connect('res/phones.db')
        self.cursor = self.db.cursor()

        self.models_list = ['Xiaomi', 'Samsung']

    # TAKE LIST OF AVAILABLE SYSTEM APPS ON PHONE MODEL
    def get_phone_apps(self, phone_model):
        try:
            apps_list = [item[0] for item in (
                self.cursor.execute(
                    '''SELECT app_name FROM app_packets WHERE ''' + phone_model + ''' = 1 
                    ORDER BY app_name''').fetchall())]
            return apps_list
        except OperationalError:
            return []

    # TAKE APP PACKET
    def get_packet_app(self, app_name, phone_model):
        try:
            packet_name = self.cursor.execute(
                '''SELECT packet_name FROM app_packets WHERE app_name = ? AND ''' + phone_model + ''' = 1''',
                (app_name,)).fetchone()
            if packet_name:
                return packet_name[0]
            return ''
        except OperationalError:
            return ''
