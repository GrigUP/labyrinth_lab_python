from lab2.packets.Enums import *


class StartCommand:
    def __init__(self, start_x, start_y, direction, sensor_direction, rotation, counter):
        self.command = Commands.START
        self.start_x = start_x
        self.start_y = start_y
        self.direction = direction
        self.sensor_direction = sensor_direction
        self.rotation = rotation
        self.counter = counter


class StopCommand:
    def __init__(self):
        self.command = Commands.STOP


class StateCommand:
    def __init__(self, robot_id, direction, x, y, sensor_direction, counter):
        self.command = Commands.ROBOT_STATE
        self.robot_id = robot_id
        if isinstance(direction, Direction):
            self.direction = direction
        self.x = x
        self.y = y
        if isinstance(sensor_direction, Direction):
            self.sensor_direction = sensor_direction
        self.counter = counter


class ConfirmCommand:
    def __init__(self, counter):
        self.command = Commands.CONFIRM
        self.time_counter = counter


class StepCommand:
    def __init__(self, step_counter):
        self.command = Commands.STEP
        self.step_counter = step_counter
