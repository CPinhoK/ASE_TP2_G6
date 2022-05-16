# Seven Segment Display with RPi

import RPi.GPIO as GPIO
from time import sleep

def setup():
    GPIO.setwarnings(False)  # Do not show any warnings
    GPIO.setmode(GPIO.BCM)  # Programming the GPIO by BCM pin number
    
    # Initialize GPIO Pins as Outputs
    GPIO.setup(13, GPIO.OUT) # A
    GPIO.setup(6, GPIO.OUT)  # B
    GPIO.setup(16, GPIO.OUT) # C
    GPIO.setup(20, GPIO.OUT) # D
    GPIO.setup(21, GPIO.OUT) # E
    GPIO.setup(19, GPIO.OUT) # F
    GPIO.setup(26, GPIO.OUT) # G
    
    GPIO.setup(20, GPIO.OUT) # High
    GPIO.setup(21, GPIO.OUT) # Low

    # String of characters storing PORT values for each digit
      

# Assigning GPIO logic by taking 'pin' value
def PORT(pin):
    if(pin&0x01 == 0x01):
        GPIO.output(13,1)            # if  bit0 of 8bit 'pin' is true, pull PIN13 high
    else:
        GPIO.output(13,0)            # if  bit0 of 8bit 'pin' is false, pull PIN13 low
    if(pin&0x02 == 0x02):
        GPIO.output(6,1)             # if  bit1 of 8bit 'pin' is true, pull PIN6 high
    else:
        GPIO.output(6,0)             #if  bit1 of 8bit 'pin' is false, pull PIN6 low
    if(pin&0x04 == 0x04):
        GPIO.output(16,1)
    else:
        GPIO.output(16,0)
    if(pin&0x08 == 0x08):
        GPIO.output(20,1)
    else:
        GPIO.output(20,0)   
    if(pin&0x10 == 0x10):
        GPIO.output(21,1)
    else:
        GPIO.output(21,0)
    if(pin&0x20 == 0x20):
        GPIO.output(19,1)
    else:
        GPIO.output(19,0)
    if(pin&0x40 == 0x40):
        GPIO.output(26,1)
    else:
        GPIO.output(26,0)
        
def send2displays(value):
    dat = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]#0,1,2,3...
    displayFlag = False # static variable: doesn't loose its
    # value between calls to function
    digit_low = dat[value & 0x0F]
    digit_high = dat[value >> 4]
    
    
    ##clean
    GPIO.output(21,0)
    GPIO.output(20,0)
    
    
    GPIO.output(13, 0) # A
    GPIO.output(6,  0) # B
    GPIO.output(16, 0) # C
    GPIO.output(20, 0) # D
    GPIO.output(21, 0) # E
    GPIO.output(19, 0) # F
    GPIO.output(26, 0) # G
    
    if(not displayFlag):   #displayFlag is 0 then send digit_low to display_low
        GPIO.output(21,1) # Low
        PORT(digit_low)

    else:                  #send digit_high to didplay_high
        GPIO.output(20,1) # High
        PORT(digit_high)
        
    displayFlag= not displayFlag


# Assigning the conditions
def loop():
    dat = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]#0,1,2,3...
    while True:
        # For 0-9 numbers
        for z in range(10):
            pin = dat[z]
            PORT(pin)
            sleep(0.8)
        sleep(1.2)
        
def mainl():
    counter = 0
    i = 0
    while(1):
        i+=1
        send2displays(counter)
        sleep(0.1)
        if(i % 4 == 0): # increment counter
            counter+=1
    return 0


# To destroy/clean-up all the pins
def destroy():     
	GPIO.cleanup()              

if __name__ == '__main__':
    setup()
    try:
        mainl()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected")
        destroy()
