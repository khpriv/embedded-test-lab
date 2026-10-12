/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2026 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <string.h>
#include <stdio.h>
#include "ssd1306.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define DEFAULT_TEMPERATURE 20
#define DEFAULT_LIMIT       80
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/

/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

I2C_HandleTypeDef hi2c1;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
uint8_t rx_byte;
char rx_buffer[64];
uint8_t rx_index = 0;

uint8_t all_on[] = {0xA5};

static int temperature = DEFAULT_TEMPERATURE;
static int limit = DEFAULT_LIMIT;
static char status[32] = "READY";

// FAULT INJECTION
static uint32_t response_delay_ms = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_I2C1_Init(void);
/* USER CODE BEGIN PFP */
void process_command(char *);
void send_response(char *);
static void reset_state(void);
static void update_display(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_I2C1_Init();
  /* USER CODE BEGIN 2 */
  SSD1306_Init(&hi2c1);
  update_display();




  char msg[] = "BOOT\r\n";
  HAL_UART_Transmit(&huart2, (uint8_t*) msg, strlen(msg), HAL_MAX_DELAY);
  /* USER CODE END 2 */

  /* Initialize leds */
  BSP_LED_Init(LED2);

  /* Initialize USER push-button, will be used to trigger an interrupt each time it's pressed.*/
  BSP_PB_Init(BUTTON_USER, BUTTON_MODE_EXTI);

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	while (1) {
    /* USER CODE END WHILE */

	/* USER CODE BEGIN 3 */
		if (HAL_UART_Receive(&huart2, &rx_byte, 1, HAL_MAX_DELAY) == HAL_OK) {
			if (rx_byte == '\r' || rx_byte == '\n') {
				if (rx_index > 0) {
					rx_buffer[rx_index] = '\0';

					process_command(rx_buffer);

					rx_index = 0;
				}
			} else {
				if (rx_index < sizeof(rx_buffer) - 1) {
					rx_buffer[rx_index++] = rx_byte;
				} else {
					/* Buffer overflow - discard current command */
					rx_index = 0;
				}
			}
		}
	}

	/* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void process_command(char *rx_buffer){

	if (strcmp(rx_buffer, "PING") == 0) {
		char response[] = "PONG\r\n";

		send_response(response);
	} else if (strcmp(rx_buffer, "GET_TEMP") == 0) {
		char response[32];


		snprintf(response, sizeof(response), "TEMP:%d\r\n",
				temperature);

		send_response(response);
	} else if (strncmp(rx_buffer, "SET_TEMP:", 9) == 0) {
		int new_temperature;

		if (sscanf(rx_buffer + 9, "%d", &new_temperature) == 1 ) {
			if (new_temperature <= limit) {
				temperature = new_temperature;
				update_display();
				send_response("OK\r\n");
			} else {
				send_response("ERR:OUT_OF_RANGE\r\n");
			}
		} else {
			send_response("ERR:INVALID_VALUE\r\n");
		}
	} else if (strcmp(rx_buffer, "GET_STATUS") == 0) {
		char response[32];

		snprintf(response, sizeof(response), "STATUS:%s\r\n", status);

		send_response(response);

	} else if (strncmp(rx_buffer, "SET_STATUS:", 11) == 0) {
		const char *new_status = rx_buffer + 11;

		if (strlen(new_status) > 0 &&
		    strlen(new_status) < sizeof(status))
		{
		    strcpy(status, new_status);
		    update_display();
		    send_response("OK\r\n");
		}
		else
		{
		    send_response("ERR:INVALID_VALUE\r\n");
		}

	} else if (strcmp(rx_buffer, "GET_LIMIT") == 0) {
		char response[32];

		snprintf(response, sizeof(response), "LIMIT:%d\r\n",
				limit);

		send_response(response);
	} else if (strncmp(rx_buffer, "SET_LIMIT:", 10) == 0) {
		int new_limit;

		if (sscanf(rx_buffer + 10, "%d", &new_limit) == 1 ) {
			limit = new_limit;
			update_display();
			send_response("OK\r\n");
		} else {
			send_response("ERR:INVALID_VALUE\r\n");
		}
	} else if (strcmp(rx_buffer, "RESET") == 0) {
		reset_state();
		update_display();
		send_response("OK\r\n");
	} else if (strncmp(rx_buffer, "FIT_DELAY:", 10) == 0) {
		char response[32];
		int new_delay;

		if (sscanf(rx_buffer + 10, "%d", &new_delay) == 1 ) {
			snprintf(response, sizeof(response), "FIT_LIMIT:%d\r\n",
					new_delay);

			send_response(response);
			response_delay_ms = new_delay;
		} else {
			send_response("ERR:INVALID_VALUE\r\n");
		}
	}
}


void send_response(char *response){
	if (response_delay_ms > 0){
		HAL_Delay(response_delay_ms);
	}
	HAL_UART_Transmit(&huart2, (uint8_t*) response,
								strlen(response),
								HAL_MAX_DELAY);
	return;
}

static void reset_state(void){
    temperature = DEFAULT_TEMPERATURE;
    limit = DEFAULT_LIMIT;
    strcpy(status, "READY");

    response_delay_ms = 0;
}

static void update_display(void)
{
    char line[32];

    SSD1306_Clear();

    snprintf(line, sizeof(line), "TEMP   : %d", temperature);
    SSD1306_SetCursor(0, 0);
    SSD1306_WriteString(line);

    snprintf(line, sizeof(line), "LIMIT  : %d", limit);
    SSD1306_SetCursor(0, 16);
    SSD1306_WriteString(line);

    SSD1306_SetCursor(0, 32);
    SSD1306_WriteString("STATUS :");

    SSD1306_SetCursor(0, 48);
    SSD1306_WriteString(status);

    SSD1306_UpdateScreen();
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */
	__disable_irq();
	while (1) {
	}
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
