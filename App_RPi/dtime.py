# Seven Segment Display with RPi
import os,subprocess,signal
import RPi.GPIO as GPIO
from time import sleep
import board
from datetime import datetime


def setup():
    GPIO.setwarnings(False)  # Do not show any warnings
    GPIO.setmode(GPIO.BCM)  # Programming the GPIO by BCM pin number
    
    #GPIO.cleanup()
    
    # Initialize GPIO Pins as Outputs
    GPIO.setup(7, GPIO.OUT) # A
    GPIO.setup(1, GPIO.OUT)  # B
    GPIO.setup(21, GPIO.OUT) # C
    GPIO.setup(20, GPIO.OUT) # D
    GPIO.setup(16, GPIO.OUT) # E
    GPIO.setup(8, GPIO.OUT) # F
    GPIO.setup(25, GPIO.OUT) # G
    
    GPIO.setup(19, GPIO.OUT) # High
    GPIO.setup(26, GPIO.OUT) # Low

    # String of characters storing PORT values for each digit
      

# Assigning GPIO logic by taking 'pin' value
def PORT(pin):
    if(pin&0x01 == 0x01):
        GPIO.output(7,1)            # if  bit0 of 8bit 'pin' is true, pull PIN13 high
    else:
        GPIO.output(7,0)            # if  bit0 of 8bit 'pin' is false, pull PIN13 low
    if(pin&0x02 == 0x02):
        GPIO.output(1,1)             # if  bit1 of 8bit 'pin' is true, pull PIN6 high
    else:
        GPIO.output(1,0)             #if  bit1 of 8bit 'pin' is false, pull PIN6 low
    if(pin&0x04 == 0x04):
        GPIO.output(21,1)
    else:
        GPIO.output(21,0)
    if(pin&0x08 == 0x08):
        GPIO.output(20,1)
    else:
        GPIO.output(20,0)   
    if(pin&0x10 == 0x10):
        GPIO.output(16,1)
    else:
        GPIO.output(16,0)
    if(pin&0x20 == 0x20):
        GPIO.output(8,1)
    else:
        GPIO.output(8,0)
    if(pin&0x40 == 0x40):
        GPIO.output(25,1)
    else:
        GPIO.output(25,0)
        
def send2displays(value,flag):
    dat = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]#0,1,2,3...
    displayFlag = flag 
    # value between calls to function
    digit_low = dat[value%10 & 0x0F]
    digit_high = dat[ int(value/10)]
    
    
    ##clean
    GPIO.output(19,0)
    GPIO.output(26,0)
    
    
    GPIO.output(7, 0) # A
    GPIO.output(1,  0) # B
    GPIO.output(21, 0) # C
    GPIO.output(20, 0) # D
    GPIO.output(16, 0) # E
    GPIO.output(8, 0) # F
    GPIO.output(25, 0) # G
    
    if(not displayFlag):   #displayFlag is 0 then send digit_low to display_low
        GPIO.output(19,1) # Low
        PORT(digit_low)

    else:                  #send digit_high to didplay_high
        GPIO.output(26,1) # High
        PORT(digit_high)
        
    displayFlag= not displayFlag
    return displayFlag
def traco():
    GPIO.output(19,1)
    GPIO.output(26,1)
    
    GPIO.output(7, 0) # A
    GPIO.output(1,  0) # B
    GPIO.output(21, 0) # C
    GPIO.output(20, 0) # D
    GPIO.output(16, 0) # E
    GPIO.output(8, 0) # F
    GPIO.output(25, 0) # G
            
    GPIO.output(25,1)
def clean():
    GPIO.output(19,0)
    GPIO.output(26,0)
    
    GPIO.output(7, 0) # A
    GPIO.output(1,  0) # B
    GPIO.output(21, 0) # C
    GPIO.output(20, 0) # D
    GPIO.output(16, 0) # E
    GPIO.output(8, 0) # F
    GPIO.output(25, 0) # G
        
       
def mainl():
    i = 0
    fl=False
	
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    flag=True
    digits=int(now.year)%100
    chain=[now.year%100,now.month,now.day,now.hour,now.minute,now.second]
    for i in range(len(chain)):
        if chain[i]<10:
            number_str = str(chain[i])
            zero_filled_number = int(number_str.zfill(2))
            print(zero_filled_number)
            chain.pop(i)
            chain.insert(i,zero_filled_number)
    print(chain)
    it = 1
    while(1):
        i+=1
        sleep(0.00001)
        print(digits,"----",i)
        fl=send2displays(digits,fl)
        if(it>len(chain)):
            it=0
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string)
            flag=True
            digits=int(now.year)%100
            chain=[now.year%100,now.month,now.day,now.hour,now.minute,now.second]
            for i in range(len(chain)):
                if chain[i]<10:
                    number_str = str(chain[i])
                    zero_filled_number = int(number_str.zfill(2))
                    chain.pop(i)
                    chain.insert(i,zero_filled_number)
            print(chain)
        if(i % 10000 == 0 ):
            iniri=0
            traco()
            while(iniri<5000):
                print("traco")
                sleep(0.00001)
                iniri+=1
            clean()
            if(it<len(chain)):
                digits=chain[it]
            it+=1
        
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
