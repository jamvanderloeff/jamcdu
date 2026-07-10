#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import logging
#logging.basicConfig(level=logging.DEBUG)
import mido
mido.set_backend('mido.backends.portmidi')
host = "JAM CDU 1"

cols = [21, 20, 26, 16, 19, 13, 12, 6]
rows = [ 2,  3,  4, 14, 15, 18, 17, 27, 22, 23, 24]
keymap = [
64,59,-1,-1,-1,-1,65,88,
63,60,-1,-1,-1,-1,66,87,
62,61,-1,-1,-1,-1,67,68,
82,51,-1,26,40,27,-1,-1,
71,78,-1,55,43,79,28,-1,
41,39,-1,30,48,46,32,18,
73,81,-1,33,34,35,23,36,
2,3,4,37,38,50,49,24,
5,6,7,25,16,19,31,20,
8,9,10,22,47,17,45,21,
52,11,12,44,57,83,53,14
]
keynames = [
"LSK6L","LSK1L"," "," "," "," ","LSK1R","LSK6R",
"LSK5L","LSK2L"," "," "," "," ","LSK2R","LSK5R",
"LSK4L","LSK3L"," "," "," "," ","LSK3R","LSK4R",
"INIT REF","RTE"," ","CLB","CRZ","DES"," "," ",
"MENU","LEGS"," ","DEP ARR","HOLD","PROG","EXEC"," ",
"N1","FIX"," ","A","B","C","D","E",
"PREV","NEXT"," ","F","G","H","I","J",
"1","2","3","K","L","M","N","O",
"4","5","6","P","Q","R","S","T",
"7","8","9","U","V","W","X","Y",
".","0","-","Z","SP","DEL","/","CLR",
]

GPIO.setmode(GPIO.BCM)
GPIO.setup(rows, GPIO.IN)
GPIO.setup(cols, GPIO.IN, pull_up_down = GPIO.PUD_UP)
pressed = set()

outport = mido.open_output(host)

while True:
    for i in range(len(rows)):
        GPIO.setup(rows[i], GPIO.OUT, initial = GPIO.LOW)
        for j in range(len(cols)):
            keycode = i * len(cols) + j
            newval = GPIO.input(cols[j]) == GPIO.LOW
            if  newval and not keycode in pressed:
                pressed.add(keycode)
                print(keynames[keycode])
                msg = mido.Message('control_change', channel = 0, control = keymap[keycode], value = 1)
                outport.send(msg)
            elif not newval and keycode in pressed:
                pressed.discard(keycode)
                msg = mido.Message('control_change', channel = 0, control = keymap[keycode], value = 0)
                outport.send(msg)
        GPIO.setup(rows[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)