import pyfirmata

port="COM7"  # yo bhaneko laptop ko port jun ma arduino connect garieako xa

board=pyfirmata.Arduino(port)

servo_x=board.get_pin('d:6:o')
servo_y=board.get_pin('d:7:o')

def get_angle(angle_x,angle_y):
 # Move servos to the mapped angles
 servo_x.write(angle_x)
 servo_y.write(angle_y)

servo_x.write(1)
servo_y.write(1)
