#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "tc74.h"
#include "driver/ledc.h"
#include "esp_err.h"

#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_OUTPUT_IO          (5) // Define the output GPIO
#define LEDC_CHANNEL            LEDC_CHANNEL_0
#define LEDC_DUTY_RES           LEDC_TIMER_13_BIT // Set duty resolution to 13 bits
#define LEDC_DUTY_25            (2500) // Set duty to 25%. ((2 ** 13) - 1) * 25% = 2500
#define LEDC_DUTY_50            (4095) // Set duty to 50%. ((2 ** 13) - 1) * 50% = 4095
#define LEDC_DUTY_100           (8191) // Set duty to 100%. ((2 ** 13) - 1) * 100% = 8191
#define LEDC_FREQUENCY          (5000) // Frequency in Hertz. Set frequency at 5 kHz

static void temp_to_led_task(void *arg) {
  // setup the sensor
  ESP_ERROR_CHECK(i2c_master_init());

  // signed integer value of 8 bits
  uint8_t temperature_value;

  // signed integer value of 8 bits
  uint8_t initial_temp;

  // signed integer value of 8 bits
  uint8_t operation_mode;

  // initial temperature value reading
  i2c_master_read_tc74_config(I2C_MASTER_NUM,&operation_mode);
  // ESP_LOGI(TAG,"Operation mode is : %d",operation_mode);
  // set normal mode for testing (200uA consuption)
  i2c_master_set_tc74_mode(I2C_MASTER_NUM, SET_NORM_OP_VALUE);
  vTaskDelay(250 / portTICK_RATE_MS);
  i2c_master_read_temp(I2C_MASTER_NUM,&initial_temp);
  ESP_LOGI(TAG,"Initial Temperature is : %d",initial_temp);
  i2c_master_read_tc74_config(I2C_MASTER_NUM,&operation_mode);
  // ESP_LOGI(TAG,"Operation mode is : %d",operation_mode);
  // set standby mode for testing (5uA consuption)
  i2c_master_set_tc74_mode(I2C_MASTER_NUM, SET_STANBY_VALUE);

  // Set the LEDC peripheral configuration
  ledc_init()
  // Set duty to 50%
  ESP_ERROR_CHECK(ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, LEDC_DUTY_50));
  // Update duty to apply the new value
  ESP_ERROR_CHECK(ledc_update_duty(LEDC_MODE, LEDC_CHANNEL));

  // periodically read temp values from sensor and changing the led intensity
  while(1){
    i2c_master_read_tc74_config(I2C_MASTER_NUM,&operation_mode);
    // ESP_LOGI(TAG,"Operation mode is : %d",operation_mode);
    // set normal mode for testing (200uA consuption)
    i2c_master_set_tc74_mode(I2C_MASTER_NUM, SET_NORM_OP_VALUE);
    vTaskDelay(250 / portTICK_RATE_MS);
    i2c_master_read_temp(I2C_MASTER_NUM,&temperature_value);
    ESP_LOGI(TAG,"Temperature is : %d",temperature_value);
    i2c_master_read_tc74_config(I2C_MASTER_NUM,&operation_mode);
    // ESP_LOGI(TAG,"Operation mode is : %d",operation_mode);
    // set standby mode for testing (5uA consuption)
    i2c_master_set_tc74_mode(I2C_MASTER_NUM, SET_STANBY_VALUE);

    if (temperature_value > initial_temp) {
      // Increase the intensity by setting the duty to 25%
      ESP_ERROR_CHECK(ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, LEDC_DUTY_100));
      // Update duty to apply the new value
      ESP_ERROR_CHECK(ledc_update_duty(LEDC_MODE, LEDC_CHANNEL));
    }
    else if (temperature_value == initial_temp)
    {
      // Maintain the intensity by keeping the duty to 50%
      ESP_ERROR_CHECK(ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, LEDC_DUTY_50));
      // Update duty to apply the new value
      ESP_ERROR_CHECK(ledc_update_duty(LEDC_MODE, LEDC_CHANNEL));
    }
    else {
      // Decrease the intensity by setting the duty to 25%
      ESP_ERROR_CHECK(ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, LEDC_DUTY_25));
      // Update duty to apply the new value
      ESP_ERROR_CHECK(ledc_update_duty(LEDC_MODE, LEDC_CHANNEL));
    }

    vTaskDelay(8000 / portTICK_RATE_MS);
  }
}

static void ledc_init(void)
{
    // Prepare and then apply the LEDC PWM timer configuration
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .timer_num        = LEDC_TIMER,
        .duty_resolution  = LEDC_DUTY_RES,
        .freq_hz          = LEDC_FREQUENCY,  // Set output frequency at 5 kHz
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ESP_ERROR_CHECK(ledc_timer_config(&ledc_timer));

    // Prepare and then apply the LEDC PWM channel configuration
    ledc_channel_config_t ledc_channel = {
        .speed_mode     = LEDC_MODE,
        .channel        = LEDC_CHANNEL,
        .timer_sel      = LEDC_TIMER,
        .intr_type      = LEDC_INTR_DISABLE,
        .gpio_num       = LEDC_OUTPUT_IO,
        .duty           = 0, // Set duty to 0%
        .hpoint         = 0
    };
    ESP_ERROR_CHECK(ledc_channel_config(&ledc_channel));
}

void app_main(void)
{
    // sensor handling task
    xTaskCreate(temp_to_led_task, "temp_to_led_task", 1024 * 2, (void *)0, 10, NULL);
}