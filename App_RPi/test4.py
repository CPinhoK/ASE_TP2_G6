# Seven Segment Display with RPi
import os,subprocess,signal
from time import sleep
from datetime import datetime


        
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
        sleep(0.0000000001)
        sleep()
        print(digits,"----",i)
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
                    print(zero_filled_number)
                    chain.pop(i)
                    chain.insert(i,zero_filled_number)
            print(chain)
        if(i % 100 == 0 ):
            iniri=0
            print("traco")
            while(iniri<50):
                print("traco")
                sleep(0.0000000001)
                iniri+=1
            
            print(it)
            if(it<len(chain)):
                digits=chain[it]
            it+=1
        
    return 0


           

if __name__ == '__main__':
    try:
        mainl()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected")
        