#!/usr/bin/python3.4

#Import required libraries
import ev3dev.ev3 as ev3
import time
from os import system
import signal
import csv
import sys

# Toggle debug output
DEBUG = False
LOG = False

# Set initial state
state       = "THINK"   # TURN, THINK, DRIVE, STOP
progress    = "INIT"    # INIT, EXEC, DONE
direction   = 'U'       # U, D, L, R

# Define inputs
btn = ev3.Button()
lightSensorLeft     = ev3.ColorSensor('in1')
lightSensorRight    = ev3.ColorSensor('in4')
lightSensorBumper   = ev3.LightSensor('in3')
gyroSensor          = ev3.GyroSensor('in2')
ls_corr         = 0
# Configure inputs
gyroSensor.mode = 'GYRO-ANG'
gs_units        = gyroSensor.units
gs_tolerance    = 15

# Check if sonsors are connected
assert lightSensorLeft.connected,   "Left light sensor is not connected (should be 'in1')"
assert lightSensorRight.connected,  "Right light sensor is not conected (should be 'in4')"
assert lightSensorBumper.connected, "Bumper sensor is not connected (should be 'in3')"
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

# Import instructions
if len(sys.argv) > 1:                   # If input arguments exist
    filename = sys.argv[1]              # Set argument as file name
else:
    filename = "instructions.csv"       # Set default file name

with open(filename, 'r')  as csvfile:   # Open CSV file
    reader = csv.reader(csvfile)        # Create CSV reader object
    instructions = list(reader)         # Store contents of CSV file in 'instructions'
index = -1;                             # Set list index at -1 so control loop can initiate by incremeting
print("Instructions loaded succesfully!")

# Define what happens if interrupted
def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    motorLeft.duty_cycle_sp     = 0
    motorRight.duty_cycle_sp    = 0
    exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Define various motor speeds
SPEED_TURN  =  40#55
SPEED_BASE  =  60
SPEED_CORR  = 0
SPEED_REV   = -60

# Define sensor thresholds
THRESHOLD_BLACK = 15    # Light sensor black
THRESHOLD_BL = 400      # Bumper sensor lower
THRESHOLD_BU = 600      # Bumper sensor upper

# Define timings
TIME_REV = 0.5         

# Define log file name
log_name  = "log" 
log_name += "_turn" + str(SPEED_TURN) 
log_name += "_base" + str(SPEED_BASE) 
log_name += "_corr" + str(SPEED_CORR) 
log_name += "_rev"  + str(SPEED_REV)
log_name += "_tol"  + str(gs_tolerance)
log_name += ".csv"

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

    # Return relative turn anglei
    if(dir_val == 90):
        return 90
    elif (dir_val == 180):
        return 173
    else:
        return dir_val 

# Turn off motors 
motorLeft.duty_cycle_sp = 0
motorRight.duty_cycle_sp = 0

# Wait for button press
print("Ready!")
while not btn.any():
    pass
ev3.Sound.beep().wait()

# Start logging
#if LOG:
#    log_arr = []

# Main control loop
while True:

    # Read sensor inputs every loop
    ls_left_val     = lightSensorLeft.value()
    ls_right_val    = lightSensorRight.value()
    ls_bumper_val   = lightSensorBumper.value()
    #gs_val          = gyroSensor.value()

    # Read motor outputs
    #mo_left_val     = motorLeft.duty_cycle_sp
    #mo_right_val    = motorRight.duty_cycle_sp

    # Print debug info if true
    if DEBUG:
        # Clear terminal before printing
        system('clear')		

        # Printing at once because ev3/ssh console is slow
        print(  "[STATE]\n"                     +
                "Current state:\t\t\t"          + state                 + '\n'      +
                "Current state progress:\t\t"   + progress              + '\n'      +
                "Current direction:\t\t"        + direction             + '\n'      +   
                '\n'                            +
                "[INPUT]\n"                     +
                "Left light sensor value:\t"    + str(ls_left_val)      + '\n'      +
                "Right light sensor value:\t"   + str(ls_right_val)     + '\n'      +
                "Bumper light sensor value:\t"  + str(ls_bumper_val)    + '\n'      +
                "Gyro sensor value:\t\t"        + str(gs_val)           + gs_units  + 
                '\n'                            + 
                '\n'                            + 
                "[OUTPUT]\n"                    +
                #"Left motor duty cycle:\t\t"    + str(mo_left_val)      + '\n'
                #"Right motor duty cycle:\t\t"   + str(mo_right_val)     + '\n'      + 
                '\n'                            +
                "[MISC]\n"                      +
                "Instruction index:\t\t"        + str(index)            + '\n'
                ) 

    # Handle button press / stop
    if btn.any():
        ev3.Sound.beep().wait()
        motorLeft.duty_cycle_sp = 0
        motorRight.duty_cycle_sp = 0
        exit()

# Stop state
# -----------------------------------------------------------------------------

    if state == "STOP":

        motorLeft.duty_cycle_sp = 0
        motorRight.duty_cycle_sp = 0

# Turn state
# -----------------------------------------------------------------------------

    if state == "TURN":
        gs_val          = gyroSensor.value()

        if progress == "INIT":
            motorLeft.duty_cycle_sp = 0
            motorRight.duty_cycle_sp = 0
            time.sleep(0.1)
            reset_val   = gs_val
            goal_ang    = control_turn(direction,goal_dir)
            goal_pol    = goal_ang/abs(goal_ang)
            progress    = "EXEC"

        if progress == "EXEC":
            dir_rel = gs_val - reset_val 
            if(dir_rel*goal_pol < abs(goal_ang)-gs_tolerance):
                motorLeft.duty_cycle_sp = SPEED_TURN*goal_pol
                motorRight.duty_cycle_sp = -SPEED_TURN*goal_pol                
            else:
                motorLeft.duty_cycle_sp = 0
                motorRight.duty_cycle_sp = 0
                time.sleep(0.1)
                progress = "DONE"        

        if progress == "DONE":
            direction = goal_dir
            if(goal_push > 0):
                state = "PUSH"
            else:
                state = "DRIVE"
            progress = "INIT"

# Drive state
# -----------------------------------------------------------------------------

    if state == "DRIVE":
        
        if progress == "INIT":
            if LOG:
                t0 = time.clock();

            # Set various control variables
            Kp = 1.2/2#0.37
            #Ki = 0
            Kd = 15 #10 
            #acc = 0
            ls_error = 0
            ls_error_prev = 0
            brake_reduce = 0;
            ls_bumper_line = False

            # Start motors
            motorLeft.duty_cycle_sp = SPEED_BASE
            motorRight.duty_cycle_sp = SPEED_BASE
            time.sleep(0.1)
            # Continue if not on line
            if not(ls_left_val < THRESHOLD_BLACK and ls_right_val < THRESHOLD_BLACK):
                progress = "EXEC"
            
        if progress == "EXEC":
            # PID control
            ls_error_prev = ls_error
            ls_error = ls_left_val - ls_right_val + ls_corr
            #acc += ls_error    
            derr = ls_error - ls_error_prev
            pid_corr = Kp*ls_error + Kd*derr
            
            #if LOG:
            #    log_arr.append([time.clock()-t0, ls_error])
            
            # If bumper detects line
            if ( not ls_bumper_line and (ls_bumper_val < THRESHOLD_BL)):
                if(goal_dir != instructions[index+1][0]):
                    brake_reduce = SPEED_CORR
                ls_bumper_line = True
 
            if(ls_left_val < THRESHOLD_BLACK and ls_right_val < THRESHOLD_BLACK):
                progress = "DONE"
            else:
                # Avoid driving motor faster than possible
                if (SPEED_BASE+abs(pid_corr)+brake_reduce <= 100):
                    motorLeft.duty_cycle_sp = SPEED_BASE+brake_reduce+(pid_corr)
                    motorRight.duty_cycle_sp = SPEED_BASE+brake_reduce-(pid_corr)
                #else:
                #    if(pid_corr>0):
                #        motorLeft.duty_cycle_sp  = 100+brake_reduce
                #        motorRight.duty_cycle_sp = SPEED_BASE+brake_reduce-(pid_corr)
                #    else:
                #        motorLeft.duty_cycle_sp  = SPEED_BASE+brake_reduce+(pid_corr)
                #        motorRight.duty_cycle_sp = 100+brake_reduce

        if progress == "DONE":
            state       = "THINK"
            progress    = "INIT"

# Think state
# -----------------------------------------------------------------------------

    if state == "THINK":

        if progress == "INIT":
            if(index+1 == len(instructions)):
                motorLeft.duty_cycle_sp = 0
                motorRight.duty_cycle_sp = 0
                progress = "DONE"
            else:
                index += 1
                goal_dir  = instructions[index][0]
                goal_push = int(instructions[index][1])
                progress  = "EXEC"

        if progress == "EXEC":
            if goal_dir != direction:
                state    = "TURN"
                progress = "INIT"
            else:
                if(goal_push == 0):
                    state    = "DRIVE"
                    progress = "INIT"
                else:
                    state    = "PUSH"
                    progress = "INIT"
        
        if progress == "DONE":
            motorLeft.duty_cycle_sp = 0
            motorRight.duty_cycle_sp = 0
            print("Goal reached!")

            #if LOG:
            #    with open(log_name,"w+") as log_csv:
            #        logw = csv.writer(log_csv,delimiter=',')
            #        logw.writerows(log_arr)
            
            state = "STOP"

# Push state
# -----------------------------------------------------------------------------
    
    if state == "PUSH": 
        if progress == "INIT":
            push_speed_increase = 2
            Kp = 1.2/2 #0.37
            #Ki = 0
            Kd = 15#10

            acc = 0
            ls_error = 0
            ls_error_prev = 0

            intersection = int(goal_push) + 1
            ls_bumper_line = False

            motorLeft.duty_cycle_sp = SPEED_BASE + push_speed_increase
            motorRight.duty_cycle_sp = SPEED_BASE + push_speed_increase

            if not(ls_left_val < THRESHOLD_BLACK and ls_right_val < THRESHOLD_BLACK):
                progress = "EXEC"

        if progress == "EXEC":
            ls_error_prev = ls_error
            ls_error = ls_left_val - ls_right_val + ls_corr
            #acc += ls_error
            derr = ls_error - ls_error_prev
            pid_corr = Kp*ls_error  + Kd*derr

            if( not ls_bumper_line and (ls_bumper_val < THRESHOLD_BL)):
                intersection -= 1
                ls_bumper_line = True
            else:
                if (SPEED_BASE+abs(pid_corr)+push_speed_increase <= 100):
                    motorLeft.duty_cycle_sp = SPEED_BASE+(pid_corr) + push_speed_increase
                    motorRight.duty_cycle_sp = SPEED_BASE-(pid_corr) + push_speed_increase

                if (ls_bumper_val > THRESHOLD_BU):
                    ls_bumper_line = False

            if (intersection == 0):
                progress = "DONE"

        if progress == "DONE":
            motorLeft.duty_cycle_sp = 0
            motorRight.duty_cycle_sp = 0
            time.sleep(0.1)
            motorLeft.duty_cycle_sp = SPEED_REV
            motorRight.duty_cycle_sp = SPEED_REV
            time.sleep(TIME_REV)
            motorLeft.duty_cycle_sp = 0
            motorRight.duty_cycle_sp = 0
            time.sleep(0.1)
            dir_inv = { 'U': 'D',
                        'D': 'U',
                        'L': 'R',
                        'R': 'L'}    
            goal_dir = dir_inv[direction]

            goal_push = 0
            state = "TURN"
            progress = "INIT"
