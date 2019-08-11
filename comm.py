"""Sends the colours in colours.npy to the Arduino via serial"""
import sys
import time
import serial
import numpy as np

# Port of Arduino
port = '/dev/cu.usbmodem14201'
# Number of LEDs to illuminate. Must be the same as NUMUSING in sketch/sktch.ino
num_using = 10

if __name__ == '__main__':
    colours = np.load('colours.npy')
    # Colours stored as floats in [0, 1]. Convert them to ints in [0, 255]
    colours = np.round(colours * 255).astype(np.int)
    
    # Convert colours to an array of bytes
    to_write = bytes([])
    for i in range(num_using):
        to_write += bytes(list(colours[i]))

    with serial.Serial(port, 9600) as ser:
        # Arduino restarts when a new serial connection is made. Give it time
        # to boot before sending any data
        time.sleep(0.5)
        # Send colours to Arduino
        written = ser.write(to_write)
        print("Written {} bytes".format(written))
