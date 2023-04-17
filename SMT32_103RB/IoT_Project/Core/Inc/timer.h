
#ifndef INC_TIMER_H_
#define INC_TIMER_H_

#include "stdint.h"
#include "main.h"
extern TIM_HandleTypeDef htim3;
void delay_us (uint16_t us);

extern int timerMS_flag;
void setTimerMS(int duration);
void timerRun();
void timerInit();
#endif /* INC_TIMER_H_ */
