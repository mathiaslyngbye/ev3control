#!/usr/bin/python3.4

def turn(start, goal):
    
    dir_cor = {
        'U': 0,
        'D': 180,
        'L': -90,
        'R': 90 }

    dir_val = dir_cor[goal] - dir_cor[start]
    dir_val = (dir_val + 180) % 360 - 180

    return dir_val

print(turn('L', 'D'))

