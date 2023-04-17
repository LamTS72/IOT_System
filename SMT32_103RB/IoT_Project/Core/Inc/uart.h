
#ifndef INC_UART_H_
#define INC_UART_H_

#include "main.h"
#include "dh11.h"
#include "scheduler.h"
#include "ctype.h"

int isDig(uint8_t ch);
int isNum(uint8_t str[], int idx);
void cmd_parser_fsm();
void cmd_check_request();
uint32_t CheckSum(char* arr, uint32_t len_str);

#endif /* INC_UART_H_ */
