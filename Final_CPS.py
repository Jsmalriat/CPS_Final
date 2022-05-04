import time
import math
from examples.web_control.web_server.picar_x import *
time.sleep(0.01)

# Ensure steering angle is 0.
dir_servo_angle_calibration(0)

# Once constraints are checked, move car to new position
def movecar(s_angle, distance):
	set_dir_servo_angle((s_angle)) 
	s_time = distance / 7.34 #num calculated with measurements
	backward(40)
	time.sleep(s_time)
	set_dir_servo_angle(0)
	stop()

# Rotates the four corners of the car for accurate positioning
def rotatepoint(angle, x, y, cx, cy):
	s = math.sin(angle)
	c = math.cos(angle)
	x -= cx
	y -= cy
	newx = (x * c) - (y * s)
	newy = (x * s) + (y * c)
	x = newx + cx
	y = newy + cy
	point = [y, x]
	return point

# Finds where the car currently is, using the angle and distance covered
def findposition(angle, dist, current_position, current_center):
	for point in current_position:
		current_position[point] = rotatepoint(angle, current_position[point][1], current_position[point][0], current_center[1], current_center[0])
		current_position[point][0] = current_position[point][0] - dist 
		current_position[point][1] = current_position[point][1] - dist
	return current_position

def checkconstr(check_position):
	# We will use a fixed speed of 20(40/2) for this experiment to try to keep velocity 
	# as close to a constant 2cm/sec, so velocity per step ≤ 𝑣𝑚𝑎𝑥 = 2 𝑐𝑚/𝑠𝑒𝑐. 

	# We will never use a servo angle greater than 30 degrees, thus 
	# keeping the constraint Steering servo angle ≤ 𝛿max =  30°.

	# Front right of car cannot hit wall/car in front of spot
	if (((check_position[1][1] >= 14) and (check_position[1][0] > 10)) or ((check_position[1][1] < 14) and (check_position[1][0] <= 10))):
		# Rear and Front right of car cannot exceed margin
		if(((check_position[1][1] > 11) and (check_position[1][0]) > -8) and ((check_position[2][1] > -11) and (check_position[2][0] > -8))):
			return 1
	else:
		return 0


def main():
	# This is the intial position of the center of the car as well as the 
	# center of the parking space. 
	initial_center = [20, 25]
	parking_center = [0, 0]
	current_center = initial_center
	
	# [(frontleft), (frontright), (backright), (backleft)]
	# car is 22cm x 16cm and space is 28cm x 20cm
	inicar_postion = [[28, 36], [12, 36], [12, 14], [28, 14]]
	space_position = [[10, 14], [-10, 14], [-10, -14], [10, -14]]
	current_position = inicar_postion

	# These are the test angles and distances for estimation.
	angles = [10, 15, 20, 30]
	move_dist = [6.0, 8.0, 10.0, 12.0]

	while (current_center != parking_center):
		for angle in angles:
			for dist in move_dist:
				check_position = findposition(angle, dist, current_position, current_center)
				if (checkconstr(check_position) == 1):
					movecar(angle, dist)
					current_position = check_position
					xcen = (current_position[1][1] - current_position[2][1])
					ycen = (current_position[3][0] - current_position[2][0])
					current_center = [ycen, xcen]

if __name__ == "__main__":
	main() 