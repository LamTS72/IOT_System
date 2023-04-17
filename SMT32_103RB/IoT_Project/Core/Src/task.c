
#ifndef SRC_TASK_C_
#define SRC_TASK_C_

#include "task.h"
#include "main.h"

void Led_Test1(){
	HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}

void Led_Test2(){
	HAL_GPIO_TogglePin(LED2_GPIO_Port, LED2_Pin);
}


#endif /* SRC_TASK_C_ */
