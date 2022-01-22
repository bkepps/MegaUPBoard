#!/usr/bin/env python

from smbus2 import SMBus
import time

# takes list formatted: 
    # ICLEDS = [  [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1],
    #             [1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1],
    #             [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 6]]
# with each number representing the color of one tri-color LED
# and with each row being for one gpio expander with IO pin 5 of bank 2 unused
# and parses into 5 bytes, one for each bank of output registers
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

i2cbus = SMBus(1)  # Create a new I2C bus -on i2c bus 1?

print("I2C bus initialized")

i2cbus.write_byte_data(ADDRIOE0, MODE, MODECFG) # Update MODE register to configure each IOExpander
print("IC1 connected")
i2cbus.write_byte_data(ADDRIOE1, MODE, MODECFG)	# Update MODE register to configure each IOExpander
print("IC2 connected")
i2cbus.write_byte_data(ADDRIOE2, MODE, MODECFG)	# Update MODE register to configure each IOExpander
print("IC3 connected")

i2cbus.write_block_data(ALLCALL, IOC0AI, ZERO5)		# set all i/o pins to outputs
print("All pins set as outputs")
i2cbus.write_byte_data(ALLCALL, OUTCONF, 0x00)		# Configure outputs of all io expanders to be open-drain
print("All outputs are open-drain")

ICLEDS = [  [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1],
            [1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1],
            [4, 2, 1, 2, 4, 5, 6, 7, 5, 1, 2, 3, 4]]
            
ICBANKS = parseLEDs(ICLEDS)

print("attempt to turn on all leds via ALLCALL, turn off 1 sec later")
i2cbus.write_block_data(ALLCALL, OP0AI, ONE5)		# set all leds to on
time.sleep(2)
i2cbus.write_block_data(ALLCALL, OP0AI, ZERO5)		# set all leds to off
time.sleep(2)

print("attempt to turn leds on according to definitions above, turn off after 20 sec")
i2cbus.write_block_data(ADDRIOE0, OP0AI, ICBANKS[1])		# set all leds to on, address each individually
i2cbus.write_block_data(ADDRIOE1, OP0AI, ICBANKS[2])
i2cbus.write_block_data(ADDRIOE2, OP0AI, ICBANKS[3])
time.sleep(3)
i2cbus.write_block_data(ADDRIOE0, OP0AI, ZERO5)		# set all leds to off, address each individually
i2cbus.write_block_data(ADDRIOE1, OP0AI, ZERO5)
i2cbus.write_block_data(ADDRIOE2, OP0AI, ZERO5)

