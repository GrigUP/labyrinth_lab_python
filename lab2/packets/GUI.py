import tkinter.filedialog
import tkinter.messagebox
from tkinter import *

from lab2.packets.Tools import *


class GUI(threading.Thread):
    def __init__(self):
        super().__init__()
        self._canvas = None
        self._sprite_size = 35
        self._map_color_route = "gray"
        self._map_color_wall = "black"
        self._robot_color = "red"
        self._map_color_target = "green"

        self._current_time_counter = 0

        # self._cm_robot = CommunicationModule("/dev/ttys001", 9600)
        self._cm_robot = CommunicationModule("COM2", 9600)
        # self._cm_dao = CommunicationModule("/dev/ttys005", 9600)
        self._cm_dao = CommunicationModule("COM4", 9600)

        self._timer_sender = Timer(10, self._send_command, None)

        self._window = Tk()

        self._is_started = False
        self._is_first_run = True

        # start button
        self._start_btn = Button(self._window, text="start emulation")
        # load map button
        self._load_map_btn = Button(self._window, text="load map")

        # start coordinate fields
        self._label_start_x = Label(self._window, text="Start").grid(row=1, column=0)

        self._robot_x = StringVar()
        self._robot_coordinate_x = Entry(self._window, textvariable=self._robot_x, insertontime=0, width=10)
        self._robot_coordinate_x.insert(0, "0")

        self._robot_y = StringVar()
        self._robot_coordinate_y = Entry(self._window, textvariable=self._robot_y, insertontime=0, width=10)
        self._robot_coordinate_y.insert(0, "0")

        # finish coordinate fields
        self._label_finish_x = Label(self._window, text="Finish").grid(row=2, column=0)

        self._finish_x = StringVar()
        self._finish_coordinate_x = Entry(self._window, textvariable=self._finish_x, insertontime=0, width=10)
        self._finish_coordinate_x.insert(0, "6")

        self._finish_y = StringVar()
        self._finish_coordinate_y = Entry(self._window, textvariable=self._finish_y, insertontime=0, width=10)
        self._finish_coordinate_y.insert(0, "2")

        # direction field
        self._direction_label = Label(self._window, text="Direction: ").grid(row=3, column=0)
        self._direction = StringVar()
        self._direction.set(Direction.N.value)
        self._direction_radio_n = Radiobutton(text=Direction.N.value, variable=self._direction, value=Direction.N.value)
        self._direction_radio_e = Radiobutton(text=Direction.E.value, variable=self._direction, value=Direction.E.value)
        self._direction_radio_w = Radiobutton(text=Direction.W.value, variable=self._direction, value=Direction.W.value)
        self._direction_radio_s = Radiobutton(text=Direction.S.value, variable=self._direction, value=Direction.S.value)

        # sensors direction field
        self._sensor_direction_label = Label(self._window, text="Sensor: ").grid(row=4, column=0)
        self._sensor_direction = StringVar()
        self._sensor_direction.set(Direction.N.value)
        self._sensor_direction_radio_n = Radiobutton(text=Direction.N.value, variable=self._sensor_direction,
                                                     value=Direction.N.value)
        self._sensor_direction_radio_e = Radiobutton(text=Direction.E.value, variable=self._sensor_direction,
                                                     value=Direction.E.value)
        self._sensor_direction_radio_w = Radiobutton(text=Direction.W.value, variable=self._sensor_direction,
                                                     value=Direction.W.value)
        self._sensor_direction_radio_s = Radiobutton(text=Direction.S.value, variable=self._sensor_direction,
                                                     value=Direction.S.value)

        # rotation
        self._rotation_label = Label(self._window, text="Rotation: ").grid(row=5, column=0)
        self._rotation = StringVar()
        self._rotation.set(Rotation.L.value)
        self._rotation_radio_l = Radiobutton(text=Rotation.L.value, variable=self._rotation,
                                             value=Rotation.L.value)
        self._rotation_radio_r = Radiobutton(text=Rotation.R.value, variable=self._rotation,
                                             value=Rotation.R.value)

        self._is_busy = False
        self._is_game_over = False

        self._map_massive = []

    def show(self):

        self._start_btn.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, columnspan=2)
        self._start_btn.bind("<Button-1>", self._start_emulation)
        self._load_map_btn.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5, columnspan=2)
        self._load_map_btn.bind("<Button-1>", self._load_map)

        self._robot_coordinate_x.grid(row=1, column=1, columnspan=2)
        self._robot_coordinate_y.grid(row=1, column=3, columnspan=2)
        self._finish_coordinate_x.grid(row=2, column=1, columnspan=2)
        self._finish_coordinate_y.grid(row=2, column=3, columnspan=2)

        self._direction_radio_n.grid(row=3, column=1)
        self._direction_radio_e.grid(row=3, column=2)
        self._direction_radio_w.grid(row=3, column=3)
        self._direction_radio_s.grid(row=3, column=4)

        self._sensor_direction_radio_n.grid(row=4, column=1)
        self._sensor_direction_radio_e.grid(row=4, column=2)
        self._sensor_direction_radio_w.grid(row=4, column=3)
        self._sensor_direction_radio_s.grid(row=4, column=4)

        self._rotation_radio_l.grid(row=5, column=1, columnspan=2)
        self._rotation_radio_r.grid(row=5, column=3, columnspan=2)

        self._window.protocol('WM_DELETE_WINDOW', self._quit)
        self._window.mainloop()

    def run(self):
        self.show()

    def stop(self):
        self._quit()

    def _quit(self):
        self._is_started = False
        self._cm_robot.stop()
        self._window.destroy()

    def _start_emulation(self, event):
        self._start_communication()

    def _update_current_parameters(self):
        self._robot_current_x = int(self._robot_x.get())
        self._robot_current_y = int(self._robot_y.get())

        self._robot_direction = Direction.get_direction_by_name(self._direction.get())
        self._robot_sensors_direction = Direction.get_direction_by_name(self._sensor_direction.get())
        self._robot_current_rotation = Rotation.get_rotation_by_name(self._rotation.get())

        self._robot_current_direction = Direction.get_direction_by_name(self._direction.get())

    def _load_map(self, event):
        tk = tkinter.filedialog.Open(self._window, filetypes=[('*.txt files', '.txt')]).show()
        map_reader = MapReader(tk)
        self._map_massive = map_reader.build_map_array(" ")
        self._render_map(self._map_massive)

    def _render_map(self, array):
        self._update_current_parameters()
        if self._canvas is None:
            self._canvas = Canvas(self._window, width=len(array) * self._sprite_size,
                                  height=len(array) * self._sprite_size)
            self._canvas.grid(row=6, columnspan=5)
        ix = 0
        iy = 0
        for arr_x in array:
            for arr_y in arr_x:
                if arr_y == 1:
                    self._draw_element(iy, ix, self._map_color_wall)
                else:
                    self._draw_element(iy, ix, self._map_color_route)

                if iy == len(array) - 1:
                    break
                iy = iy + 1
            if ix == len(array) - 1:
                break
            ix = ix + 1
            iy = 0

        if self._robot_current_x is None or self._robot_current_y is None:
            self._render_robot(int(self._robot_x.get()), int(self._robot_y.get()), self._robot_current_direction, self._robot_sensors_direction)
        else:
            self._render_robot(self._robot_current_x, self._robot_current_y, self._robot_current_direction, self._robot_sensors_direction)
        self._draw_element(int(self._finish_x.get()), int(self._finish_y.get()), self._map_color_target)

    def _render_robot(self, x, y, direction, sensor_direction):
        self._draw_element(x, y, self._robot_color)
        robot_radius = int(self._sprite_size / 2) + 1

        # convert to canvas coordinate
        x = x * self._sprite_size
        y = y * self._sprite_size

        robot_center_x = x + robot_radius
        robot_center_y = y + robot_radius

        if direction == Direction.W:
            robot_side_x = robot_center_x - robot_radius
            robot_side_y = robot_center_y
        elif direction == Direction.E:
            robot_side_x = robot_center_x + robot_radius
            robot_side_y = robot_center_y
        elif direction == Direction.N:
            robot_side_x = robot_center_x
            robot_side_y = robot_center_y - robot_radius
        else:
            robot_side_x = robot_center_x
            robot_side_y = robot_center_y + robot_radius

        robot_sensor_x = None
        robot_sensor_y = None

        if sensor_direction == Direction.W:
            robot_sensor_x = robot_center_x - robot_radius
            robot_sensor_y = robot_center_y
        elif sensor_direction == Direction.E:
            robot_sensor_x = robot_center_x + robot_radius
            robot_sensor_y = robot_center_y
        elif sensor_direction == Direction.N:
            robot_sensor_x = robot_center_x
            robot_sensor_y = robot_center_y - robot_radius
        else:
            robot_sensor_x = robot_center_x
            robot_sensor_y = robot_center_y + robot_radius

        self._canvas.create_line(robot_center_x, robot_center_y, robot_side_x, robot_side_y, width=7)
        self._canvas.create_line(robot_center_x, robot_center_y, robot_sensor_x, robot_sensor_y, width=3, fill='green')

    def _draw_element(self, x, y, color):
        self._canvas.create_rectangle(1 + x * self._sprite_size, 1 + y * self._sprite_size,
                                      x * self._sprite_size + self._sprite_size,
                                      y * self._sprite_size + self._sprite_size, fill=color)

    def _render_game_over_dialog(self):
        tkinter.messagebox.showinfo("Игра закончена, Вы превосходны!",
                                    "\nКоличество шагов: " + str(self._current_time_counter))

    def _start_communication(self):
        self._cm_robot.start()

        emu_command = None
        if self._is_started:
            emu_command = StopCommand()
        else:
            emu_command = StartCommand(self._robot_current_x, self._robot_current_y, self._robot_current_direction,
                                       self._robot_sensors_direction, self._robot_current_rotation, 0)

        self._cm_robot.send(JsonHelper.to_json(emu_command))
        self._check_command()

    def _check_command(self):
        data = self._cm_robot.receive()
        object = JsonHelper.from_json(data)

        # confirmation start/stop emulation
        if isinstance(object, ConfirmCommand):
            if self._is_first_run:
                self._start_btn.config(text="stop emulation")
                self._is_started = True
                self._is_first_run = False
                self._timer_sender.start()
                return
            self._is_started = not self._is_started
            if self._is_started:
                self._timer_sender.start()
                self._start_btn.config(text="stop emulation")
            else:
                self._timer_sender.stop()
                self._start_btn.config(text="start emulation")

        # get state from robot
        if isinstance(object, StateCommand):
            self._current_time_counter = object.counter
            self._cm_dao.send(data)

            if int(self._finish_coordinate_x.get()) == int(object.x) and int(self._finish_coordinate_y.get()) == int(
                    object.y):
                self._is_game_over = True

            self._is_busy = False

            if self._map_massive[self._robot_current_y][self._robot_current_x] == 1:
                map_color = self._map_color_wall
            else:
                map_color = self._map_color_route

            self._draw_element(self._robot_current_x, self._robot_current_y, map_color)

            self._robot_current_x = int(object.x)
            self._robot_current_y = int(object.y)
            self._robot_current_direction = object.direction
            self._robot_sensors_direction = object.sensor_direction
            self._render_robot(self._robot_current_x, self._robot_current_y, self._robot_current_direction, self._robot_sensors_direction)

    def _send_command(self):
        if self._is_game_over:
            stop_command = StopCommand()
            self._cm_robot.send(JsonHelper.to_json(stop_command))
            self._render_game_over_dialog()
            self._is_game_over = False
        if not self._is_busy:
            step_command = StepCommand(self._current_time_counter)
            self._cm_robot.send(JsonHelper.to_json(step_command))
            self._is_busy = True

        self._check_command()

#
# gui = GUI()
# gui.show()
