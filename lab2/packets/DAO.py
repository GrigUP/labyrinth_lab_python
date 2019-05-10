import mysql.connector
from lab2.packets.Tools import *


class DAO(threading.Thread):
    def __init__(self, host, username, password, database):
        super().__init__()

        self._cm = CommunicationModule("COM14", 9600)
        # self._cm = CommunicationModule("/dev/ttys004", 9600)

        self._is_started = True

        self._config = {
            'user': username,
            'password': password,
            'host': host,
            'database': 'python_labs',
        }

    def init(self):
        delete_rows_query = "DELETE FROM robot_state;"
        self._execute_query(delete_rows_query)

    def run(self):
        print("Start DAO thread.")
        while self._is_started:
            data = self._cm.receive()
            object = JsonHelper.from_json(data)
            if isinstance(object, StateCommand):
                self.add_state(object)

    def _getConnection(self):
        connection = None
        try:
            connection = mysql.connector.connect(**self._config)
        except mysql.connector.Error as err:
            print(err)
        return connection

    def _execute_query(self, query):
        connection = self._getConnection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def add_robot(self, robot_name, type):
        query = "INSERT INTO robots (robot_name, robot_type) VALUES ('{}', '{}');".format(robot_name, type)
        print(query)
        self._execute_query(query)

    def add_robot_type(self, type_name):
        query = "INSERT INTO type_of_robots (type_name) VALUES ('{}');".format(type_name)
        print(query)
        self._execute_query(query)

    def add_state(self, state):
        if isinstance(state, StateCommand):
            query = "INSERT INTO robot_state (robot_id, x, y, direction, step) VALUES ('{}', '{}', '{}', '{}', '{}');" \
                .format(state.robot_id, state.x, state.y, state.direction.value, state.counter)
            print(query)
            self._execute_query(query)
