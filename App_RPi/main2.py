#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2022  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import time
import board
import adafruit_tc74

i2c = board.I2C()
print(i2c)
tc = adafruit_tc74.TC74(i2c, address=0x4d)

while True:
    print(f"Temperature: {tc.temperature} C")
    time.sleep(0.5)

# import time
# import smbus

# i2c_ch = 1

# # TMP102 address on the I2C bus
# i2c_address = 0x4d

# # Register addresses
# reg_temp = 0x00
# reg_config = 0x01

# # Calculate the 2's complement of a number
# def twos_comp(val, bits):
    # if (val & (1 << (bits - 1))) != 0:
        # val = val - (1 << bits)
    # return val

# # Read temperature registers and calculate Celsius
# def read_temp():

    # # Read temperature registers
    # val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    # # NOTE: val[0] = MSB byte 1, val [1] = LSB byte 2
    # #print ("!shifted val[0] = ", bin(val[0]), "val[1] = ", bin(val[1]))

    # temp_c = (val[0] << 4) | (val[1] >> 4)
    # #print (" shifted val[0] = ", bin(val[0] << 4), "val[1] = ", bin(val[1] >> 4))
    # #print (bin(temp_c))

    # # Convert to 2s complement (temperatures can be negative)
    # temp_c = twos_comp(temp_c, 12)

    # # Convert registers value to temperature (C)
    # temp_c = temp_c * 0.0625

    # return temp_c

# # Initialize I2C (SMBus)
# bus = smbus.SMBus(i2c_ch)

# # Read the CONFIG register (2 bytes)
# val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
# print("Old CONFIG:", val)

# # Set to 4 Hz sampling (CR1, CR0 = 0b10)
# val[1] = val[1] & 0b00111111
# val[1] = val[1] | (0b10 << 6)

# # Write 4 Hz sampling back to CONFIG
# bus.write_i2c_block_data(i2c_address, reg_config, val)

# # Read CONFIG to verify that we changed it
# val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
# print("New CONFIG:", val)

# # Print out temperature every second
# while True:
    # temperature = read_temp()
    # print(round(temperature, 2), "C")
    # time.sleep(1)
