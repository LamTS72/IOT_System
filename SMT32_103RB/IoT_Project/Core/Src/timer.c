#include "timer.h"


void delay_us (uint16_t us){
	__HAL_TIM_SET_COUNTER(&htim3,0);  // set the counter value a 0
	while (__HAL_TIM_GET_COUNTER(&htim3) < us);  // wait for the counter to reach the us input in the parameter
}

int timerMS_flag = 0;
int timerMS_counter = 0;
void setTimerMS(int duration){
	timerMS_counter = duration;
	timerMS_flag = 0;
}
void timerRun(){
	if(timerMS_counter > 0){
		timerMS_counter--;
		if(timerMS_counter <= 0){
			timerMS_flag = 1;
		}
	}
}

void timerInit(){
	setTimerMS(20);
}
