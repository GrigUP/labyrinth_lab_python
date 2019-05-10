from lab2.packets.Tools import *


class Robot(threading.Thread):

    def __init__(self):
        super().__init__()

        self._robot_id = 2

        self._is_started = True
        self._cm = CommunicationModule("COM3", 9600)
        # self._cm = CommunicationModule("/dev/ttys002", 9600)

        self._local_time_counter = 0

        map_reader = MapReader("E:/Учеба/Python/lab2/resources/map.txt")
        self._map_massive = map_reader.build_map_array(" ")

        self._map_heap = {"": ""}

        self._current_x = None
        self._current_y = None
        self._current_direction = None
        self._sensor_direction = None
        self._rotation = None

        self._min_route_counter = 65635
        self._correct_direction = None

        self._is_first_run = True
        self._is_analization_mode = True
        self._is_correction_mode = False
        self._last_direction = None

    def stop(self):
        self._is_started = False
        print("Stop robot thread.")

    def run(self):
        print("Start robot thread.")
        while self._is_started:
            receive_data = self._cm.receive()
            receive_data = JsonHelper.from_json(receive_data)
            if isinstance(receive_data, StartCommand):
                confirm_command = ConfirmCommand(receive_data.counter)

                self._current_x = int(receive_data.start_x)
                self._current_y = int(receive_data.start_y)
                self._current_direction = Direction.get_direction_by_name(receive_data.direction)
                self._sensor_direction = Direction.get_direction_by_name(receive_data.sensor_direction)
                self._rotation = Rotation.get_rotation_by_name(receive_data.rotation)

                self._cm.send(JsonHelper.to_json(confirm_command))
            if isinstance(receive_data, StopCommand):
                confirm_command = ConfirmCommand(self._local_time_counter)
                self._cm.send(JsonHelper.to_json(confirm_command))
                self._is_started = False
                self._cm.stop()
            if isinstance(receive_data, StepCommand):
                self._make_step()
                self._local_time_counter += 1
                state_command = StateCommand(self._robot_id, self._current_direction, self._current_x, self._current_y,
                                             self._sensor_direction, self._local_time_counter)
                self._cm.send(JsonHelper.to_json(state_command))

    def _make_step(self):
        next_coordiante = self._get_next_coordinate(self._current_x, self._current_y, self._sensor_direction)
        next_step_x = next_coordiante["next_step_x"]
        next_step_y = next_coordiante["next_step_y"]

        if self._is_first_run:
            self._last_direction = self._current_direction
            self._is_first_run = False

        if self._is_analization_mode:
            self._search_correct_way()
            self._rotate()
            if self._current_direction is self._last_direction:
                self._min_route_counter = 65635
                self._is_analization_mode = False
                self._is_correction_mode = True
                return
            return

        if self._is_correction_mode:
            if self._current_direction is not self._correct_direction:
                self._rotate()
                return
            self._correct_direction = None
            self._is_correction_mode = False
            return

        self._mark_route()
        self._move()
        self._last_direction = self._current_direction
        self._is_analization_mode = True

    def _get_next_coordinate(self, x, y, direction):
        if direction == Direction.W:
            next_step_x = self._current_x - 1
            next_step_y = self._current_y

        if direction == Direction.E:
            next_step_x = self._current_x + 1
            next_step_y = self._current_y

        if direction == Direction.N:
            next_step_x = self._current_x
            next_step_y = self._current_y - 1

        if direction == Direction.S:
            next_step_x = self._current_x
            next_step_y = self._current_y + 1
        return {"next_step_x": next_step_x, "next_step_y": next_step_y}

    def _mark_route(self):
        code = str(self._current_x) + "_" + str(self._current_y)
        if code not in self._map_heap:
            self._map_heap[code] = 1
            return
        else:
            self._map_heap[code] += 1

    def _search_correct_way(self):
        next_coordinate = self._get_next_coordinate(self._current_x, self._current_y, self._sensor_direction)
        next_step_x = next_coordinate["next_step_x"]
        next_step_y = next_coordinate["next_step_y"]

        if self._is_wall(next_step_x, next_step_y):
            return

        code = str(next_step_x) + "_" + str(next_step_y)
        if code not in self._map_heap:
            self._correct_direction = self._sensor_direction
            self._min_route_counter = 0
        else:
            if self._map_heap[code] < self._min_route_counter:
                self._min_route_counter = self._map_heap[code]
                self._correct_direction = self._sensor_direction

    def _is_wall(self, x, y):
        if 0 > x or x > len(self._map_massive) - 1 or 0 > y or y > len(self._map_massive) - 1 or self._map_massive[y][
            x] == 1:
            return True
        return False

    def _rotate(self):
        if self._rotation == Rotation.R:
            if self._current_direction == Direction.W:
                self._current_direction = Direction.N
            elif self._current_direction == Direction.E:
                self._current_direction = Direction.S
            elif self._current_direction == Direction.N:
                self._current_direction = Direction.E
            elif self._current_direction == Direction.S:
                self._current_direction = Direction.W

            if self._sensor_direction == Direction.W:
                self._sensor_direction = Direction.N
            elif self._sensor_direction == Direction.E:
                self._sensor_direction = Direction.S
            elif self._sensor_direction == Direction.N:
                self._sensor_direction = Direction.E
            elif self._sensor_direction == Direction.S:
                self._sensor_direction = Direction.W

            return

        if self._rotation == Rotation.L:
            if self._current_direction == Direction.W:
                self._current_direction = Direction.S
            elif self._current_direction == Direction.E:
                self._current_direction = Direction.N
            elif self._current_direction == Direction.N:
                self._current_direction = Direction.W
            elif self._current_direction == Direction.S:
                self._current_direction = Direction.E

            if self._sensor_direction == Direction.W:
                self._sensor_direction = Direction.S
            elif self._sensor_direction == Direction.E:
                self._sensor_direction = Direction.N
            elif self._sensor_direction == Direction.N:
                self._sensor_direction = Direction.W
            elif self._sensor_direction == Direction.S:
                self._sensor_direction = Direction.E

            return

    def _move(self):
        if self._current_direction == Direction.W:
            self._current_x -= 1
        if self._current_direction == Direction.E:
            self._current_x += 1
        if self._current_direction == Direction.N:
            self._current_y -= 1
        if self._current_direction == Direction.S:
            self._current_y += 1

# robot = Robot()
# robot.start()
