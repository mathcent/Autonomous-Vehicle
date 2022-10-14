
from controller import Robot, Camera


robot = Robot()
camera = Camera("camera")

timestep = int(robot.getBasicTimeStep())
camera.enable(timestep)
camera.wb_camera_get_image()
while robot.step(timestep) != -1:

    pass


