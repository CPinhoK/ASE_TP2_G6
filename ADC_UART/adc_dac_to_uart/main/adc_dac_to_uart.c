#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "driver/adc.h"
#include "driver/dac.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/uart.h"
#include "string.h"
#include "esp_adc_cal.h"

//ADC AND DAC
#define DAC_CHANNEL     DAC_CHANNEL_2  //GPIO26
#define ADC_CHANNEL     ADC1_CHANNEL_7 //GPIO27
#define NO_OF_SAMPLES   64   
#define DEFAULT_VREF    1100

static const adc_bits_width_t width = ADC_WIDTH_BIT_12;
static esp_adc_cal_characteristics_t *adc_chars;
static const adc_atten_t atten = ADC_ATTEN_DB_0;
static const adc_unit_t unit = ADC_UNIT_1;

//UART
static const int RX_BUF_SIZE = 1024;

#define TXD_PIN (GPIO_NUM_4)
#define RXD_PIN (GPIO_NUM_5)

char * increment_voltage(uint8_t output_data) {
        //int     read_raw;
        esp_err_t r;

        char s[1024]="";
        char buffer[1024];
        dac_output_voltage( DAC_CHANNEL, output_data );
        //r = adc2_get_raw( ADC_CHANNEL, width, &read_raw);
        
        uint32_t adc_reading = 0;
        //Multisampling
        for (int i = 0; i < NO_OF_SAMPLES; i++) {
            int raw;
            r=adc2_get_raw(ADC_CHANNEL, width, &raw);
            adc_reading += raw;
        }
        adc_reading /= NO_OF_SAMPLES;
        //Convert adc_reading to voltage in mV
        uint32_t voltage = esp_adc_cal_raw_to_voltage(adc_reading, adc_chars);
        
        if ( r == ESP_OK ) {
            //printf("%d: %d\n", output_data, read_raw );
            snprintf(buffer, 10, "%d", output_data);
            strcat(s,buffer);
            strcat(s," : ");
            snprintf(buffer, 10, "%d", adc_reading);
            strcat(s,buffer);
            strcat(s," : ");
            snprintf(buffer, 10, "%d", voltage);
            strcat(s,buffer);
            strcat(s,"mV");
            //printf("string is :%s\n", s);

        } 
        else {
            printf("%s\n", esp_err_to_name(r));
            return "Error";
        }
    
    char * fstr=malloc(strlen(s) + 1);
    strcpy(fstr, s);
    //printf("fstr:%s\n",fstr);
    return fstr;
}
void init_uart(void) {
    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    // We won't use a buffer for sending data.
    uart_driver_install(UART_NUM_1, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART_NUM_1, &uart_config);
    uart_set_pin(UART_NUM_1, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
}

int sendData(const char* logName,const char* data)
{
    const int len = strlen(data);
    const int txBytes = uart_write_bytes(UART_NUM_1, data, len);
    ESP_LOGI(logName, "Wrote %d bytes", txBytes);
    return txBytes;
}

static void tx_task(void *arg)
{
    uint8_t output_data=0;
    static const char *TX_TASK_TAG = "TX_TASK";
    esp_log_level_set(TX_TASK_TAG, ESP_LOG_INFO);
    while (1) {
        //printf(arg);
        char* data = increment_voltage(output_data++);
        vTaskDelay(5);
        //printf("data:%s",data);
        sendData(TX_TASK_TAG,data);
        free(data);
        if (output_data>0xfe){
            output_data=0;
        }
        vTaskDelay(2000 / portTICK_PERIOD_MS);
    }
}

static void rx_task(void *arg)
{
    static const char *RX_TASK_TAG = "RX_TASK";
    esp_log_level_set(RX_TASK_TAG, ESP_LOG_INFO);
    uint8_t* data = (uint8_t*) malloc(32+1);
    ESP_LOGI(RX_TASK_TAG,"Started receiving");
    while (1) {
        const int rxBytes = uart_read_bytes(UART_NUM_1, data, RX_BUF_SIZE, 1000 / portTICK_RATE_MS);
        //printf("rxBYTES: %d\n",rxBytes);
        //printf("DATA: %s\n",data);
        if (rxBytes > 0) {
            data[rxBytes] = 0;
            ESP_LOGI(RX_TASK_TAG, "         OutputData : ReadRaw : Voltage");
            ESP_LOGI(RX_TASK_TAG, "Read %d bytes: '%s'", rxBytes, data);
            ESP_LOG_BUFFER_HEXDUMP(RX_TASK_TAG, data, rxBytes, ESP_LOG_INFO);
        }else{
        }
    }
    free(data);
}

void init_adc_dac(void){
    static const char *ADC_INIT = "ADC_INIT";
    esp_err_t r;
    gpio_num_t adc_gpio_num, dac_gpio_num;

    r = adc2_pad_get_io_num( ADC_CHANNEL, &adc_gpio_num );
    assert( r == ESP_OK );
    r = dac_pad_get_io_num( DAC_CHANNEL, &dac_gpio_num );
    assert( r == ESP_OK );
    
    ESP_LOGI(ADC_INIT,"ADC channel %d @ GPIO %d, DAC channel %d @ GPIO %d.", ADC_CHANNEL, adc_gpio_num,
                DAC_CHANNEL + 1, dac_gpio_num );

    dac_output_enable( DAC_CHANNEL );

    //be sure to do the init before using adc2.
    ESP_LOGI(ADC_INIT,"adc_init...");

    adc2_config_channel_atten( ADC_CHANNEL, ADC_ATTEN_11db );

    //vTaskDelay(2 * portTICK_PERIOD_MS);
    vTaskDelay(100);
}


void inner_uart_transmission(void)
{
    TaskHandle_t tx_h = NULL ;
    TaskHandle_t rx_h = NULL ;
    xTaskCreate(rx_task, "uart_rx_task", 1024*2, NULL, configMAX_PRIORITIES, &rx_h);
    xTaskCreate(tx_task, "uart_tx_task", 1024*8, NULL, configMAX_PRIORITIES-1, &tx_h);
}

static void print_char_val_type(esp_adc_cal_value_t val_type)
{
    static const char *valtypetag = "VAL_TYPE";
    if (val_type == ESP_ADC_CAL_VAL_EFUSE_TP) {
        ESP_LOGI(valtypetag,"Characterized using Two Point Value");
    } else if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
        ESP_LOGI(valtypetag,"Characterized using eFuse Vref");
    } else {
        ESP_LOGI(valtypetag,"Characterized using Default Vref");
    }
}

void app_main(void)
{
    static const char *MAIN = "MAIN";

    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    esp_adc_cal_value_t val_type = esp_adc_cal_characterize(unit, atten, width, DEFAULT_VREF, adc_chars);
    print_char_val_type(val_type);

    init_adc_dac(); //init adc and dac
    init_uart(); //init uart
    ESP_LOGI(MAIN,"start conversion.\n");
    inner_uart_transmission();
}
