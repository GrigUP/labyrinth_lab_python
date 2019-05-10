from enum import Enum

class Commands(Enum):
    START = "START ROBOT"
    STOP = "STOP ROBOT"
    CONFIRM = "CONFIRM_COMMAND"
    ROBOT_STATE = "ROBOT_STATE"
    STEP = "STEP ROBOT"


class Direction(Enum):
    W = "WEST"
    S = "SOUTH"
    E = "EAST"
    N = "NORTH"


    def get_direction_by_name(name):
        name = str(name)
        if name == "WEST":
            return Direction.W
        elif name == "SOUTH":
            return Direction.S
        elif name == "EAST":
            return Direction.E
        elif name == "NORTH":
            return Direction.N

class Rotation(Enum):
    L = "LEFT"
    R = "RIGHT"

    def get_rotation_by_name(name):
        name = str(name)
        if name == "LEFT":
            return Rotation.L
        elif name == "RIGHT":
            return Rotation.R