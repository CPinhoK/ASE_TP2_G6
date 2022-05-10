# ASE_TP2_G6
ADC_UART/I2C_PWM/SPI_DAC Mini Projects for the class of Arquiteturas para Sistemas Embutidos regarding the ESP32 architecture.

App_RPi Mini Projects for the class of Arquiteturas para Sistemas Embutidos regarding the RaspberryPi architecture.

# Application 1: I2C + PWM
In this app we use I2C communication to get the temperature reading from the TC74 temperature sensor. Then with this value, we use the led pwm controller to control the luminosity intensity of a led. So if the temperature is increased the luminosity gets stronger, otherwise it gets weaker.
In this module when the temperature sensor is not reading he is set to stanby mode, by doing this we minimize his power consuption.

### Logical schematic diagram
![plot](./I2C_PWM/I2C-PWM.png)

# Application 2: SPI + DAC
In this app the ESP32-DevKitC SPI Master Driver is used to write data to the device 25LC040A SPI EEPROM , this data is then read and set as the output for the DAC channel 1. Each two iterations the eeprom is written with incrementing or decrementing values depending how it was before. In the begining of the program you can choose if you want to overwrite the data currently in the eeprom. 
### Logical schematic diagram
![plot](./SPI_DAC/SPI-DAC.png)

# Application 3: ADC + UART
In this app the ESP32-DevKitC the DAC module is used to create a voltage that is read by the ADC then the data read is sent to the Uart that has the TXD_PIN and RXD_PIN shorted so it will comunicate with itself after the data is received it will be echoed.At the next transmission the DAC is set to higher voltage and so on.
### Logical schematic diagram
![plot](./ADC_UART/ADC-UART.png)


## Possible breadboard implementation
![plot](./top.jpg)

![plot](./side.jpg)
