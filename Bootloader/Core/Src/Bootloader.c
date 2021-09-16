/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "crc.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#define 	App_Adress			  0x8004000UL
#define	  Reset_Handler			(App_Adress + 4)
<<<<<<< Updated upstream
=======

#define   APP_END           (uint8_t*) 0x801FFFBUL  // App end address
#define   ROM_LEN						(uint32_t) (APP_END - App_Adress +1u )//APP size on flash
#define   ROM_LEN_WORD			(uint32_t) (ROM_LEN / 4u) //CRC Calculation process 4bytes per iternation
                                                      //so we get how much Words there are in our App

#define   ExpectedCRCValue  *(uint32_t *) 0x0801FFFC //Where we store the postBuild generated Checksum
volatile uint32_t CRCValue = 0;


>>>>>>> Stashed changes
typedef   void (*pFunction) (void);

 __attribute__((section(".noinit"))) volatile uint32_t test ;

<<<<<<< Updated upstream
=======



 




>>>>>>> Stashed changes
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
void  JumpToMain(void);

//FLASH_EraseInitTypeDef eraseInit = {
  //  FLASH_TYPEERASE_PAGES,  /*!< Pages erase only (Mass erase is disabled)*/
    //0,                      /*!< Select banks to erase when Mass erase is enabled.*/
    //0x08003000,              /*!< Initial FLASH page address to erase when mass erase is disabled
                                 //This parameter must be a number between Min_Data = 0x08000000 and Max_Data = FLASH_BANKx_END 
                                 //(x = 1 or 2 depending on devices)*/
    //1                       /*!< Number of pagess to be erased.
                                 //This parameter must be a value between Min_Data = 1 and Max_Data = (max number of pages - value of initial page)*/
//};
 

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

void JumpToMain(void){
	
uint32_t reset_Handler =*(volatile uint32_t *)Reset_Handler;
uint32_t msp_val = *(volatile uint32_t *)App_Adress;

pFunction Jump= (pFunction) reset_Handler;

	  HAL_RCC_DeInit();
	  HAL_DeInit();

	  SysTick->CTRL = 0;
	  SysTick->LOAD = 0;
	  SysTick->VAL = 0;

SCB->VTOR = App_Adress;


__set_MSP(msp_val);

Jump();

}
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
  MX_CRC_Init();
  MX_USART1_UART_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
<<<<<<< Updated upstream
=======
    CRCValue =HAL_CRC_Calculate(&hcrc, (uint32_t*)App_Adress,( uint32_t ) ROM_LEN_WORD);
  /*HAL_FLASH_Unlock();
  HAL_FLASHEx_Erase(&eraseInit, &pageError);
  HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, 0x08002000,CRCValue);
  HAL_FLASH_Lock();*/
  
  /*  
    if(CRCValue == ExpectedCRCValue ){
    HAL_GPIO_WritePin(GPIOA,GPIO_PIN_4,1);
    HAL_Delay(2000);
    HAL_GPIO_WritePin(GPIOA,GPIO_PIN_4,0);

 }*/

  
>>>>>>> Stashed changes
  
	  if(HAL_GPIO_ReadPin(GPIOB,GPIO_PIN_12)         ||      //Boutton in toggled during start-up

    (test==1)                                      ||      //Bootloader was issued by main app after softreset

    CRCValue != ExpectedCRCValue                   ||
    
    *(volatile uint32_t *)App_Adress==0xFFFF       //||      //App wasn't flashed
  
    )
  
  {
        
        HAL_GPIO_WritePin(GPIOA,GPIO_PIN_4,1);
        HAL_Delay(2000);
        test=0;
        JumpToMain();
        
  }
	else {
    JumpToMain();}
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
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

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

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
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
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

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
