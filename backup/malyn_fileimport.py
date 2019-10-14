#!/usr/bin/python3.4

import ev3dev.ev3 as ev3
from time import sleep
from os import system
import signal

# Toggle debug output
DEBUG = False

# Set initial state
state       = "LINE"    # TURN, LINE, STOP
progress    = "INIT"    # INIT, EXEC, DONE
direction   = 'U'       # U, D, L, R

# Define inputs
btn = ev3.Button()
lightSensorLeft     = ev3.ColorSensor('in1')
lightSensorRight    = ev3.ColorSensor('in4')
gyroSensor          = ev3.GyroSensor('in2')

# Configure inputs
gyroSensor.mode = 'GYRO-ANG'
gs_units = gyroSensor.units
gs_tolerance = 3
index = -1;

# Unused inputs
#ultrasonicSensor = ev3.UltrasonicSensor('in2')
#touchSensor =  ev3.TouchSensor('in2')

# Check if sonsors are connected
assert lightSensorLeft.connected,   "Left light sensor is not connected (should be 'in1')"
assert lightSensorRight.connected,  "Right light sensor is not conected (should be 'in4')"
assert gyroSensor.connected,        "Gyro sensor is not connected (should be 'in2')"
print("Inputs loaded succesfully!")

# Define used outputs
motorLeft   = ev3.LargeMotor('outA')
motorRight  = ev3.LargeMotor('outD')

# Configure outputs
motorLeft.run_direct()
motorRight.run_direct()
motorLeft.polarity  = "normal"
motorRight.polarity = "normal"
print("Outputs loaded succesfully!")

#import ev3dev.ev3 as ev3	        # Import ev3dev.ev3 with the alias ev3
from time import sleep
import signal
import os
import csv
import sys


# Import instructions
if len(sys.argv) > 1:                   # If input arguments exist
    filename = sys.argv[1]              # Set argument as file name
else:
    filename = "instructions.csv"       # Set default file name

with open(filename, 'r')  as csvfile:   # Open CSV file
    reader = csv.reader(csvfile)        # Create CSV reader object
    instructions = list(reader)         # Store contents of CSV file in 'instructions'
print("Instructions loaded succesfully!")

# Define what happens if interrupted
def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    motorLeft.duty_cycle_sp     = 0
    motorRight.duty_cycle_sp    = 0
    exit(0)

# Run signal handler
signal.signal(signal.SIGINT, signal_handler)

# Define various control variables
SPEED_TURN = 20
SPEED_SLOW = 30
SPEED_BASE = 50
SPEED_FAST = 70
THRESHOLD_BLACK = 15

# Relative turn angle function
def control_turn(dir_start, dir_goal):
    # Dictionary of angle correction
    dir_cor = { 'U': 0,
                'D': 180,
                'L': -90,
                'R': 90 }    
    
    # Calculate turn value (angle)
    dir_val = dir_cor[dir_goal] - dir_cor[dir_start]
    dir_val = (dir_val + 180) % 360 - 180    

    # Return relative turn angle
    return dir_val 

# Turn off motors 
motorLeft.duty_cycle_sp = 0
motorRight.duty_cycle_sp = 0

# Wait for button press
print("Ready!")
while not btn.any():
    pass
ev3.Sound.beep().wait()

# Main control loop
while True:

    # Read sensor inputs every loop
    ls_left_val     = lightSensorLeft.value()
    ls_right_val    = lightSensorRight.value()
    gs_val          = gyroSensor.value()

    # Read motor outputs
    mo_left_val    = motorLeft.duty_cycle_sp
    mo_right_val    = motorRight.duty_cycle_sp

    # Print debug info if true
    if DEBUG:
        # Clear terminal before printing
        system('clear')		

        # Printing at once because ev3/ssh console is slow
        print(  "[STATE]\n" +
                "Current state:\t\t\t"          + state             + '\n'      +
                "Current state progress:\t\t"   + progress          + '\n'      +
                "Current direction:\t\t"        + direction         + '\n'      +   
                '\n' +
                "[INPUT]\n" +
                "Left light sensor value:\t"    + str(ls_left_val)  + '\n'      +
                "Right light sensor value:\t"   + str(ls_right_val) + '\n'      +
                "Gyro sensor value:\t\t"        + str(gs_val)       + gs_units  + '\n'  + 
                '\n' + 
                "[OUTPUT]\n" +
                "Left motor duty cycle:\t\t"      + str(mo_left_val)  + '\n'
                "Right motor duty cycle:\t\t"     + str(mo_right_val)
                ) 

    # Handle button press / stop
    if btn.any():
        ev3.Sound.beep().wait()
        motorLeft.duty_cycle_sp = 0
        motorRight.duty_cycle_sp = 0
        exit()

    # Test: Stop state
    if state == "STOP":
        motorLeft.duty_cycle_sp = 0
        motorRight.duty_cycle_sp = 0

    # Test: Turn state
    if state == "TURN":
 
        if progress == "INIT":
            reset_val   = gs_val
            goal_ang    = control_turn(goal_dir, 'L')
            goal_pol    = goal_ang/abs(goal_ang)
            progress    = "EXEC"

        if progress == "EXEC":
            dir_rel = gs_val - reset_val 
            if(dir_rel*goal_pol < abs(goal_ang)-gs_tolerance):
                motorLeft.duty_cycle_sp = SPEED_TURN*goal_pol
                motorRight.duty_cycle_sp = -SPEED_TURN*goal_pol                
            else:
                progress = "DONE"        

        if progress == "DONE":
            direction   = goal_dir
            state       = "DRIVE"
            progress    = "INIT"

    # Test: Drive state
    if state == "LINE":
        
        if progress == "INIT":
            Kp = 1.25/2
            Ki = 0.01
            Kd = 5
            
            acc = 0
            ls_error = 0
            ls_error_prev = 0

            motorLeft.duty_cycle_sp = SPEED_BASE
            motorRight.duty_cycle_sp = SPEED_BASE
            
            if not(ls_left_val < THRESHOLD_BLACK and ls_right_val < THRESHOLD_BLACK):
                progress = "EXEC"
            
        if progress == "EXEC":
            ls_error_prev = ls_error
            ls_error = ls_left_val - ls_right_val
            acc += ls_error    
            derr = ls_error - ls_error_prev
            
            pid_corr = Kp*ls_error + Ki*acc + Kd*derr

            if(ls_left_val < THRESHOLD_BLACK and ls_right_val < THRESHOLD_BLACK):
                progress = "DONE"
            else:
                if (SPEED_BASE+abs(pid_corr) <= 100):
                    motorLeft.duty_cycle_sp = SPEED_BASE+(pid_corr)
                    motorRight.duty_cycle_sp = SPEED_BASE-(pid_corr)

        if progress == "DONE":
            state       = "THINK"
            progress    = "INIT"

    # Test: Think
    if state == "THINK":
        if progress == "INIT"
            if(index+1 == len(instructions):
                progress == "DONE"
            else:
                index += 1
                goal_dir = instructions[index][0]
                goal_push   = instructions[index][1]
                progress = "EXEC"

        if progress == "EXEC"
            if goal_dir != direction:
                state == "TURN"
                progress == "INIT"
            else:
                state == "DRIVE"
                progress == "INIT"
        
        if progress == "DONE"
            print("Goal reached!")
            state == "STOP"
                
