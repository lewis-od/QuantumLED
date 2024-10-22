"""Sends the colours in colours.npy to the Arduino via serial"""
import os
import sys
import time
import serial
import numpy as np

# Port of Arduino
port = '/dev/cu.usbmodem14201'

if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(this_dir, os.pardir, 'output')

    # Load colours generated by lab.py
    colours = np.load(os.path.join(output_dir, 'colours.npy'))
    
    to_write = bytes(list(colours.flatten()))
    
    with serial.Serial(port, 9800) as ser:
        # Arduino restarts when a new serial connection is made. Give it time
        # to boot before sending any data
        time.sleep(1.5)
        # Send colours to Arduino
        written = ser.write(to_write)
        print("Written {} bytes".format(written))
        # For some reason we need to sleep before disconnecting too (?)
        time.sleep(0.25)
