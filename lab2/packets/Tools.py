import threading

from serial import *

from lab2.packets.Serializers import *


class CommunicationModule:

    def __init__(self, port, baudrate):
        self._is_started = False
        self._serial_port = Serial(port, baudrate)

    def start(self):
        if not self._is_started and not self._serial_port.is_open:
            self._serial_port.open()
            self._is_started = True

    def stop(self):
        self._is_started = False
        self._serial_port.close()

    def receive(self):
        data = self._serial_port.readline()
        data = data.decode().replace("\n", "")
        print("RECEIVE: ", data, "timestamp: ", int(time.time()*1000))
        return data

    def send(self, message):
        print("SEND: ", message, "timestamp: ", int (time.time()*1000))
        message += "\n"
        self._serial_port.write(bytes(message.encode()))

    def is_started(self):
        return self._is_started

class JsonHelper:

    def from_json(json_string):
        obj = None
        if Commands.CONFIRM.name in json_string:
            obj = json.loads(json_string, cls=ConfirmCommandSerializer)

        elif Commands.ROBOT_STATE.name in json_string:
            obj = json.loads(json_string, cls=StateCommandSerializer)

        elif Commands.START.name in json_string:
            obj = json.loads(json_string, cls=StartCommandSerializer)

        elif Commands.STOP.name in json_string:
            obj = json.loads(json_string, cls=StopCommandSerializer)

        elif Commands.STEP.name in json_string:
            obj = json.loads(json_string, cls=StepCommandSerializer)

        return obj

    def to_json(obj):
        result_str = None

        if isinstance(obj, StartCommand):
            result_str = json.dumps(obj, cls=StartCommandSerializer)

        elif isinstance(obj, StopCommand):
            result_str = json.dumps(obj, cls=StopCommandSerializer)

        elif isinstance(obj, StateCommand):
            result_str = json.dumps(obj, cls=StateCommandSerializer)

        elif isinstance(obj, StepCommand):
            result_str = json.dumps(obj, cls=StepCommandSerializer)

        elif isinstance(obj, ConfirmCommand):
            result_str = json.dumps(obj, cls=ConfirmCommandSerializer)

        return result_str

class MapReader:
    def __init__(self, map_file_name):
        self._file_name = map_file_name

    def build_map_array(self, separator):
        self._open()
        file = self._file
        lines = file.readlines()
        map_matrix = []
        for line in lines:
            row = (self._split_line(line, separator))
            map_matrix.append(row)
        self._close()

        return map_matrix

    def _open(self):
        self._file = open(self._file_name, "r")

    def _close(self):
        self._file.close();

    def _split_line(self, line, separator):
        line = str(line)
        nums = line.split(separator)
        array = []
        for num in nums:
            if num is "\n":
                continue
            array.append(int(num))

        return array


class Timer(threading.Thread):
    def __init__(self, milliseconds, method, arg):
        threading.Thread.__init__(self)
        self._interval = milliseconds
        self._is_started = False
        self._start_time = int(time.time() * 1000)
        self._method = method
        self._arg = arg

    def stop(self):
        self._is_started = False

    def start(self):
        if not self._is_started:
            self._is_started = True
            super().start()


    def run(self):
        while self._is_started:
            current_time = int(time.time() * 1000)
            if (current_time - self._start_time > self._interval):
                if self._arg is None:
                    self._method()
                else:
                    self._method(self._arg)
                self._start_time = current_time
