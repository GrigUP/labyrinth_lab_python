import json
import time

from lab2.packets.Commands import *


class ConfirmCommandSerializer(json.JSONEncoder, json.JSONDecoder):
    def default(self, z):
        if isinstance(z, ConfirmCommand):
            return dict(command=z.command.value, time_counter=z.time_counter)

    def decode(self, s):
        if Commands.CONFIRM.name in s:
            json_str = str(s)
            counter = json_str[SerializeHelper.find_last_index(json_str, 'nter": '):json_str.index('}')]
            return ConfirmCommand(counter)
        else:
            return None


class StateCommandSerializer(json.JSONEncoder, json.JSONDecoder):
    def default(self, z):
        if isinstance(z, StateCommand):
            return dict(command=z.command.value, robot_id=z.robot_id, direction=z.direction.value, x=z.x, y=z.y,
                        sensor_direction=z.sensor_direction.value, counter=z.counter)

    def decode(self, s):
        if Commands.ROBOT_STATE.name in s:
            json_str = str(s)
            robot_id = json_str[
                       SerializeHelper.find_last_index(json_str, '"robot_id": '):json_str.index(', "direction":')]
            direction = json_str[SerializeHelper.find_last_index(json_str, '"direction": "'):json_str.index('", "x":')]
            x = json_str[SerializeHelper.find_last_index(json_str, '"x": '):json_str.index(', "y":')]
            y = json_str[SerializeHelper.find_last_index(json_str, '"y": '):json_str.index(', "sensor_direction":')]
            sensor_direction = json_str[
                               SerializeHelper.find_last_index(json_str, '"sensor_direction": "'):json_str.index(
                                   '", "counter":')]
            counter = json_str[SerializeHelper.find_last_index(json_str, '"counter": '):json_str.index('}')]

            return StateCommand(robot_id, Direction.get_direction_by_name(direction), x, y,
                                Direction.get_direction_by_name(sensor_direction), counter)
        else:
            return None


class StepCommandSerializer(json.JSONEncoder, json.JSONDecoder):
    def default(self, z):
        if isinstance(z, StepCommand):
            return dict(command=z.command.value, step_counter=z.step_counter)

    def decode(self, s):
        if Commands.STEP.name in s:
            json_str = str(s)
            counter = json_str[SerializeHelper.find_last_index(json_str, 'nter": '):json_str.index('}')]
            return StepCommand(counter)
        else:
            return None


class StartCommandSerializer(json.JSONEncoder, json.JSONDecoder):
    def default(self, z):
        if isinstance(z, StartCommand):
            return dict(command=z.command.value, start_x=z.start_x, start_y=z.start_y, direction=z.direction.value,
                        sensor_direction=z.sensor_direction.value, rotation=z.rotation.value, time_counter=z.counter)

    def decode(self, s):
        if Commands.START.name in s:
            json_str = str(s)
            start_x = json_str[SerializeHelper.find_last_index(json_str, '"start_x": '):json_str.index(', "start_y":')]
            start_y = json_str[SerializeHelper.find_last_index(json_str, '"start_y": '):json_str.index(', "direction')]
            dirr = json_str[
                   SerializeHelper.find_last_index(json_str, '"direction": "'):json_str.index('", "sensor_direction"')]
            sensor_dirr = json_str[
                          SerializeHelper.find_last_index(json_str, '"sensor_direction": "'):json_str.index(
                              '", "rotation"')]
            rotation = json_str[
                       SerializeHelper.find_last_index(json_str, '"rotation": "'):json_str.index('", "time_counter"')]
            time_counter = json_str[SerializeHelper.find_last_index(json_str, '"time_counter": '):json_str.index('}')]

            return StartCommand(start_x, start_y, dirr, sensor_dirr, rotation, time_counter)
        else:
            return None


class StopCommandSerializer(json.JSONEncoder, json.JSONDecoder):
    def default(self, z):
        if isinstance(z, StopCommand):
            return dict(command=z.command.value)

    def decode(self, s):
        if Commands.STOP.name in s:
            return StopCommand()
        else:
            return None


class SerializeHelper:
    def find_last_index(src, string):
        return str(src).find(string) + len(string)
