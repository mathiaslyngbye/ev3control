#!/bin/bash
if [ "$1" = "--run" ] || [ "$1" = "-r" ];
then
    echo "Running ev3control.py remotely...";
    # Run program
    sshpass -p 'ai1rockz' ssh ai1@192.168.0.1 python3 ev3control.py
else
    echo "Flashing ev3control.py...";
    # Use sshpass to single command copy main file
    sshpass -p 'ai1rockz' scp ./ev3control.py ai1@192.168.0.1:~/
fi


