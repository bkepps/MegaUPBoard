#!/usr/bin/env python

#from smbus2 import SMBus
#import time

def parseLEDs(ICLEDS):
    ICDATA = [0, 0, 0]

    ICBANKS = [ [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    for i in range(3):
        for j in range(len(ICLEDS[i])):
            ICDATA[i] = ICDATA[i] << 3
            ICDATA[i] = ICDATA[i] + ICLEDS[i][j]
            
    for i in range(3):
        for j in range(len(ICBANKS[i])):
            for k in range(8):
                ICBANKS[i][j] = ICBANKS[i][j] << 1
                if (j == 2) and (k == 5):
                    continue
                ICBANKS[i][j] = ICBANKS[i][j] + (ICDATA[i] & 0b100000000000000000000000000000000000000)
                ICDATA[i] = ICDATA[i] << 1
            ICBANKS[i][j] = ICBANKS[i][j] >> 38
    return ICBANKS

# Define registers values from datasheet
IOC0 = 0x18	# I/O configuration register 0
IOC0AI = 0x98	# I/O configuration register 0 with Auto Increment bit set
OP0 = 0x08	# Output Port register 0
OP0AI = 0x88	# Output Port Register 0 with AI bit set
OUTCONF = 0x28	# output structure configuration
ALLBNK = 0x29	# control all banks
MODE = 0x2A	# PCA9698 mode selection

# Define various addresses
ALLCALL = 0b1101110	# address for All Call
ADDRIOE0 = 0x21		# address of IOExpander 0
ADDRIOE1 = 0x22		# address of IOExpander 1
ADDRIOE2 = 0x24		# address of IOExpander 2

# Define mode config
MODECFG = 0x00001011

ZERO5 = [0x00, 0x00, 0x00, 0x00, 0x00]
ONE5 = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]


ICLEDS = [  [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1],
            [1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 6]]
            
ICBANKS = parseLEDs(ICLEDS)
        
        #skip IO2_5
for i in range(3):
    for j in range(len(ICBANKS[i])):
        print("{0:b}".format(ICBANKS[i][j]))