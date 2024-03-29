from os import chdir
from sqlite3 import connect, OperationalError
import requests


class DatabaseTaker:
    def __init__(self):
        # TRYING TO LOAD NEWEST DATABASE
        self.download_link = 'https://github.com/m0t9/SAR/raw/master/res/phones.db'
        self.newest_db = False
        self.load_database()

        self.db = connect('res/phones.db')
        self.cursor = self.db.cursor()
        self.models_list = sorted([i[0].capitalize()
                                   for i in self.cursor.execute('SELECT * FROM app_packets').description[2:]])

    # TAKE LIST OF AVAILABLE SYSTEM APPS ON PHONE MODEL
    def get_phone_apps(self, phone_model):
        try:
            apps_list = [item[0] for item in (
                self.cursor.execute(
                    f'SELECT app_name FROM app_packets WHERE {phone_model} = 1 ORDER BY app_name').fetchall())]
            return apps_list
        except OperationalError:
            return []

    # TAKE APP PACKET
    def get_packet_app(self, app_name, phone_model):
        try:
            packet_name = self.cursor.execute(
                f'SELECT packet_name FROM app_packets WHERE app_name = ? AND {phone_model} = 1',
                (app_name,)).fetchone()
            if packet_name:
                return packet_name[0]
            return ''
        except OperationalError:
            return ''

    # DB LOADER
    def load_database(self):
        try:
            content = (requests.get(self.download_link)).content
            with open(r'res/phones.db', "wb") as file:
                file.write(content)
                self.newest_db = True
        except Exception:
            pass
