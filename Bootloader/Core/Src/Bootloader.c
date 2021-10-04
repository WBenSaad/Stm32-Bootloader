/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "crc.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private typedef -----------------------------------------------------------*/
typedef   void (*pFunction) (void);

/* Private define ------------------------------------------------------------*/
#define 	App_Adress			  0x8004000UL
#define	  Reset_Handler			(App_Adress + 4)

#define   APP_END           (uint8_t*) 0x8011FFBUL                  //App end address
#define   ROM_LEN						(uint32_t) (APP_END - App_Adress +1u )  //APP size on flash
#define   ROM_LEN_WORD			(uint32_t) (ROM_LEN / 4u)               //CRC Calculation process 4bytes per iternation
                                                                    //so we get how much Words there are in our App

#define   ExpectedCRCValue  *(uint32_t *) 0x08011FFCUL //Where we store the postBuild generated Checksum

#define Max_Buffer_Size		300 

 __attribute__((section(".noinit"))) volatile uint32_t test ; //Shared Memory between APP and Bootloader

/* Private variables ---------------------------------------------------------*/
volatile uint32_t CRCValue = 0;
uint32_t buffer2[Max_Buffer_Size] ;
uint32_t buffer[Max_Buffer_Size];

/* Private function prototypes -----------------------------------------------*/
void JumpToMain(void);
void Bootloader_flash(uint32_t* buffer);
void memory_erase(void);
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

void memory_erase(void){
	
  HAL_FLASH_Unlock();
  uint32_t PAGEError;
	static FLASH_EraseInitTypeDef EraseInitStruct;
	EraseInitStruct.TypeErase   = FLASH_TYPEERASE_PAGES;
	EraseInitStruct.PageAddress = App_Adress  ;
	EraseInitStruct.NbPages     = 55 ;
	
	HAL_FLASHEx_Erase(&EraseInitStruct,&PAGEError);

  HAL_FLASH_Lock();
	
}

void Bootloader_flash(uint32_t* buffer){
    static uint32_t mem_address = App_Adress;
		
		int remaining=0;
		
    //First Receive the Packet Length
		HAL_UART_Receive(&huart1,(uint8_t*)&buffer[0],1,HAL_MAX_DELAY);
		uint8_t packet_length=*(uint8_t *)&buffer[0];
    
    //Now receive the entire Packet
		HAL_UART_Receive(&huart1,(uint8_t*)buffer2,packet_length,HAL_MAX_DELAY);
		
    
    uint8_t payload_length= (packet_length - 4) ;			//Basically Data length is size of Packet received minus CRC WORD
	  uint32_t packet_CRC =*(uint32_t*)(&buffer2[( payload_length / 4 )]);//CRC is the last Word on our packet
		
		//
		uint32_t CRCValue=HAL_CRC_Calculate(&hcrc,(uint32_t*)buffer2 ,(payload_length / 4));

		// We calulate the CRC of the received Packet before flashing it and if doesnt match 
    // the Checksum we have ,we request a resend from the HOST on the PC
		while(CRCValue!=packet_CRC){
			
			HAL_UART_Transmit(&huart1,(uint8_t*)"0",1,HAL_MAX_DELAY);
			HAL_UART_Receive(&huart1,(uint8_t*)buffer2,packet_length,HAL_MAX_DELAY);
			CRCValue=HAL_CRC_Calculate(&hcrc,(uint32_t*)buffer2,(payload_length / 4));
		}
			HAL_UART_Transmit(&huart1,(uint8_t*)"1",1,HAL_MAX_DELAY);
		
			HAL_FLASH_Unlock();
			
		// We got the number of words that forms our payload because we will Flash a Word at a time	
			int numofwords = (payload_length/4)+((payload_length % 4)!=0);
			
			while(remaining  < numofwords ){
			
			HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD,mem_address,buffer2[remaining]);
			
				
				
			mem_address += 4;
			remaining+=1;
	}
			
		 HAL_FLASH_Lock();
		
}


/**************************Jump to App implementation ************************************/

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


/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{


  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();


  /* Configure the system clock */
  SystemClock_Config();

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_CRC_Init();
  MX_USART1_UART_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
  
  CRCValue =HAL_CRC_Calculate(&hcrc, (uint32_t*)App_Adress,( uint32_t ) ROM_LEN_WORD);

  
	  if(HAL_GPIO_ReadPin(GPIOB,GPIO_PIN_12)         ||      //Boutton in toggled during start-up

    (test==1)                                      ||      //Bootloader was issued by main app after softreset

    CRCValue != ExpectedCRCValue                   ||      //Invalid Checksum =>Invalid Image
    
    *(volatile uint32_t *)App_Adress==0xFFFF               //no app in memory
  
    )
  
  {
        
      while (1)
      {
    
		    static int i=0;
        if(i==0){
		      memory_erase(); //We start by erasing the location of our new app during our first iteration 
		      i=1;              
        }
    
        HAL_UART_Receive(&huart1,(uint8_t*)&buffer[0],1,HAL_MAX_DELAY);		
		    switch(buffer[0])
		    {
			    case 0x1:                      //0x1 for Flashing 
				    Bootloader_flash(buffer);
				    break;
			    
          case 0x9:                     //0x9 flashing done
				    JumpToMain();
            break;
			  }
	    }	
  }
	else 
  {
   JumpToMain();
  }
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

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

}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
