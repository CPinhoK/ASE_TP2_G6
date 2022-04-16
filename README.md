# ASE_TP2_G6
Mini Projects for the class of Arquiteturas para Sistemas Embutidos regarding the ESP32 architecture.

# Application 1: I2C + PWM


# Application 2: SPI + DAC
In this app the ESP32-DevKitC SPI Master Driver is used to write data to the device 25LC040A SPI EEPROM , this data is then read and set as the output for the DAC channel 1. Each two iterations the eeprom is written with incrementing or decrementing values depending how it was before.  
### Logical schematic diagram
![plot](./SPI_DAC/SPI-DAC.png)

# Application 3: ADC + UART
In this app the ESP32-DevKitC the DAC module is used to create a voltage that is read by the ADC then the data read is sent to the Uart that has the TXD_PIN and RXD_PIN shorted so it will comunicate with itself after the data is received it will be echoed.
### Logical schematic diagram
![plot](./ADC_UART/ADC-UART.png)