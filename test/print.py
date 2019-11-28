#!/bin/python3
# Define various motor speeds
SPEED_TURN  =  45
SPEED_BASE  =  80
SPEED_CORR  = -20
SPEED_REV   = -30

# Define sensor thresholds
THRESHOLD_BLACK = 15    # Light sensor black
THRESHOLD_BL = 400      # Bumper sensor lower
THRESHOLD_BU = 600      # Bumper sensor upper

# Define log file name
log_name  =  "log" 
log_name +=  "_turn" + str(SPEED_TURN) 
log_name +=  "_base" + str(SPEED_BASE) 
log_name +=  "_corr" + str(SPEED_CORR) 
log_name +=  "_rev"  + str(SPEED_REV)
log_name +=  ".csv"
print(log_name)
