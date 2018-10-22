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
print("Calibration current is " + my_drive.axis0.controller.config.calibration_current + "A")

# Set some hardware parameters temporarily
print("setting some hardware parameters temporarily")
my_drive.config.brake_resistance = 0.5
my_drive.axis0.motor.config.pole_pairs = 4

my_drive.axis0.encoder.config.cpr = 400000

# Calibrate
print("starting calibration")
my_drive.axis0.encoder.use_index = True
my_drive.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

print("waiting for calibration to end...")
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Closed loop control 
print("Changing state to closed loop control")
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

curr_pos = mydrive.axis0.encoder.pos_estimate
print("current position is " + curr_pos + "ticks")

new_pos = curr_pos + 400000
print("sending to " + new_pos + "ticks") 
my_drive.axis0.controller.pos_setpoint = new_pos




