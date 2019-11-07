#!/bin/bash


if [ "$1" = "--login" ] || [ "$1" = "-l" ];
then
    echo "Attempting ssh connection...";
    sshpass -p 'ai1rockz' ssh ai1@192.168.0.1
elif [ "$1" = "--run" ] || [ "$1" = "-r" ];
then
    echo "Running ev3control.py remotely...";
    sshpass -p 'ai1rockz' ssh ai1@192.168.0.1 python3 ev3control.py
else
    echo "Flashing ev3control.py and instructions.csv...";
    sshpass -p 'ai1rockz' scp ./ev3control.py ai1@192.168.0.1:~/
    sshpass -p 'ai1rockz' scp ./instructions.csv ai1@192.168.0.1:~/
fi


