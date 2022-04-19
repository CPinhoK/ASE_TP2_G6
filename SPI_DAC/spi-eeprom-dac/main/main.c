#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "eeprom.h"


#include <stdio.h>
#include <driver/dac.h>
#include <driver/dac_common.h>


#include <time.h>
static const char *TAG = "MAIN";

void dump(uint8_t *dt, int n);
void write_data(EEPROM_t dev, char in);
void app_main(void)
{
	ESP_LOGI(TAG, "EEPROM_MODEL=%s", "25LC040A 4-Kbit SPI Bus Serial EEPROM");
	EEPROM_t dev;
	spi_master_init(&dev);
	int32_t totalBytes = eeprom_TotalBytes(&dev);
	ESP_LOGI(TAG, "totalBytes=%d Bytes",totalBytes);
	int16_t pageSize = eeprom_PageSize(&dev);
	ESP_LOGI(TAG, "pageSize=%d Bytes",pageSize);
	int16_t lastPage = eeprom_LastPage(&dev);
	ESP_LOGI(TAG, "lastPage=%d Page",lastPage);

	
	// Get Status Register
	uint8_t reg;
	esp_err_t ret;
	ret = eeprom_ReadStatusReg(&dev, &reg);
	if (ret != ESP_OK) {
		ESP_LOGE(TAG, "ReadStatusReg Fail %d",ret);
		while(1) { vTaskDelay(1); }
	} 
	ESP_LOGI(TAG, "readStatusReg : 0x%02x", reg);

	// Write Data
	uint8_t wdata[512];
	// Read Data
	uint8_t rbuf[512];
	// Buffer Length
	int len;

	srand(time(NULL));   // Initialization, should only be called once.
	ESP_LOGI(TAG, "Should there be a first write ? (y/n)");
	//let the use choose
	char in;
	in=getchar(); // To consume the newline
	while(in==255){
		in=getchar();  
		vTaskDelay(1);
	} 
	//printf("%d\n",in);

	if(in==(int)'y'){
		ESP_LOGI(TAG, "Should the memory be filled with random values (y/n)");
		//let the use choose
		char r;
		r=getchar(); // To consume the newline
			while(r==255){
			r=getchar();  
			vTaskDelay(1);
		} 
		ESP_LOGI(TAG, "Writing Memory");
		// Write Byte
		if(r==(int)'y'){
			ESP_LOGI(TAG, "Writing Memory with random values");
			for (int i=0; i<512; i++) {
				wdata[i]= rand() % 0xff ; // rand() % (max - min + 1) + min;
			}
		}else{
			for (int i=0; i<512; i++) {
				wdata[i]=0xff-i;	
			}
		}  
		for (int addr=0; addr<512;addr++) {
			len =  eeprom_WriteByte(&dev, addr, wdata[addr]);
			ESP_LOGD(TAG, "WriteByte(addr=%d) len=%d", addr, len);
			if (len != 1) {
				ESP_LOGE(TAG, "WriteByte Fail addr=%d", addr);
				while(1) { vTaskDelay(1); }
			}
		}
	}else{ESP_LOGI(TAG, "Skip Write Memory");}
	
	ESP_LOGI(TAG, "Read Memory");
	// Read 512 byte from Address=0
	memset(rbuf, 0, 512);
	len =  eeprom_Read(&dev, 0, rbuf, 512);
	if (len != 512) {
		ESP_LOGE(TAG, "Read Fail");
		while(1) { vTaskDelay(1); }
	}
	ESP_LOGI(TAG, "Read Data: len=%d", len);
	dump(rbuf, 512);



	//DAC Configuration
	dac_channel_t channel_25=DAC_CHANNEL_1;
	ret=dac_output_enable(channel_25);
    ESP_LOGI(TAG,"Channel was enabled - fuction returned %d\n",ret);
	if (ret != ESP_OK) {
		ESP_LOGE(TAG, "DAC Enable Failed %d",ret);
		while(1) { vTaskDelay(1); }
	}
	
	int it=0;
	int flag=0;
	while(1){
		if (it % 2 == 0)
		{
			if(flag){
				write_data(dev,'>');
				ESP_LOGI(TAG,"\nEEPROM set incrementing values\n");
			}
			else{
				write_data(dev,'<');
				ESP_LOGI(TAG,"\nEEPROM set decrementing values\n");
			}
			flag=!flag;
			it=0;
		}

		memset(rbuf, 0, 512);
		len =  eeprom_Read(&dev, 0, rbuf, 512);

		for(int i=0;i<len;i++){
			ESP_LOGI(TAG,"Val - %02x\n",rbuf[i]);
			vTaskDelay(1);//main freq
			ret=dac_output_voltage(channel_25,(u_int8_t)rbuf[i]);
				if (ret != ESP_OK) {
					ESP_LOGE(TAG, "Set of DAC output failed %u",ret);
					while(1) { vTaskDelay(1); }
				}
        	ESP_LOGI(TAG,"DAC VOLTAGE %02x\r",(u_int8_t) rbuf[i]);
		} 
		it++;
	}
}
void write_data(EEPROM_t dev, char in){
	// Write Data
	uint8_t wdata[512];
	int len;
	// Write Byte
	if (in == '>'){
		for (int i=0; i<512; i++) {
			wdata[i]=i;	
		}
	}else if (in == '<'){
		for (int i=0; i<512; i++) {
			wdata[i]=0xff-i;	
		}
	}else{
		return;
	}


	for (int addr=0; addr<512;addr++) {
		len =  eeprom_WriteByte(&dev, addr, wdata[addr]);
		ESP_LOGD(TAG, "WriteByte(addr=%d) len=%d", addr, len);
		if (len != 1) {
			ESP_LOGE(TAG, "WriteByte Fail addr=%d", addr);
			while(1) { vTaskDelay(1); }
		}
	}
}

void dump(uint8_t *dt, int n)
{
	uint16_t clm = 0;
	uint8_t data;
	uint32_t saddr =0;
	uint32_t eaddr =n-1;

	printf("--------------------------------------------------------\n");
	uint32_t addr;
	for (addr = saddr; addr <= eaddr; addr++) {
		data = dt[addr];
		if (clm == 0) {
			printf("%05x: ",addr);
		}

		printf("%02x ",data);
		clm++;
		if (clm == 16) {
			printf("| \n");
			clm = 0;
		}
	}
	printf("--------------------------------------------------------\n");
}