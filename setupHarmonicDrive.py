#!/usr/bin/env python3

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")
print("Calibration current is " + str(my_drive.axis1.motor.config.calibration_current) + "A")

# Set some hardware parameters temporarily
print("setting some hardware parameters temporarily")

my_drive.config.brake_resistance = 0.3
my_drive.axis0.motor.config.pole_pairs = 4
my_drive.axis0.motor.config.resistance_calib_max_voltage = 5.0

my_drive.axis0.encoder.config.cpr = 4000

print("position gain:",my_drive.axis0.controller.config.pos_gain, " (counts/s)/counts")
print("vel integrator gain:",my_drive.axis0.controller.config.vel_integrator_gain, " A/((counts/s) * s)")
print("velocity gain gain:",my_drive.axis0.controller.config.vel_gain, " A/(counts/sec)")
my_drive.axis0.controller.config.vel_integrator_gain = 0
my_drive.axis0.controller.config.vel_gain = 0.0001


# Calibrate
print("starting calibration")
my_drive.axis1.encoder.config.use_index = True
my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

print("waiting for calibration to end...")
while my_drive.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)


my_drive.save_configuration()

print("Motor phase resistance is: " + str(my_drive.axis1.motor.config.phase_resistance) + " ohms.")

# Closed loop control 
print("Changing state to closed loop control")
my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

while my_drive.axis1.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
    print("axis errors are:")
    print(hex(my_drive.axis1.error))	
    print("motor errors are:")
    print(hex(my_drive.axis1.motor.error))
    print("encoder errors are:")
    print(hex(my_drive.axis1.encoder.error))
    quit()
    time.sleep(0.1)


print("current state is " + str(my_drive.axis1.current_state))

curr_pos = my_drive.axis1.encoder.pos_estimate
print("current position is " + str(curr_pos) + " ticks")

new_pos = curr_pos + 400000
print("sending to " + str(new_pos) + " ticks") 
my_drive.axis1.controller.pos_setpoint = new_pos

while(1):
	print("position: ", my_drive.axis0.encoder.pos_estimate)

