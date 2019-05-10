from lab2.packets.GUI import GUI
from lab2.packets.Robot import Robot
from lab2.packets.DAO import DAO

dao = DAO("127.0.0.1", "root", "root", "python_labs")
dao.init()
dao.start()

robot = Robot()
robot.start()

gui = GUI()
gui.show()

