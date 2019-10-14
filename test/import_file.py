#!/usr/bin/python3.4

#import ev3dev.ev3 as ev3	        # Import ev3dev.ev3 with the alias ev3
from time import sleep
import signal
import os
import csv
import sys

# Print the current working directory
#print(os.getcwd())

# Import direction file system argument
if len(sys.argv) > 1:               # If input arguments exist
    filename = sys.argv[1]          # Set argument as file name
else:
    filename = "instructions.csv"   # Set default file name

# Import robot directions from CSV
with open(filename, 'r')  as csvfile:    # Open CSV file
    reader = csv.reader(csvfile)        # Create CSV reader object
    instructions = list(reader)         # Store first line of CSV file

index = -1
# Print all elements of 'directions'
while(True):
    index += 1
    if index == len(instructions):
        print("Success")
        break
    else:
        print(instructions[index][0])



