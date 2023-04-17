#include "uart.h"

uint8_t buffer_byte;
uint8_t buffer[MAX_BUFFER_SIZE];
uint8_t index_buffer = 0;
uint8_t buffer_flag = 0;
uint8_t idx_buffer = 0;

int mode = INIT;
uint8_t cmd_data[MAX_CMD_SIZE];
uint8_t cmd_data_index = 0;
uint8_t request_flag = 0;
uint8_t request_check = 0;

void rst_buffer(){
	for(int i=0; i<MAX_BUFFER_SIZE; i++){
		buffer[i] = ' ';
	}
	idx_buffer = 0;
	index_buffer =0;
	cmd_data_index = 0;
}

int isDig(uint8_t ch){
	if(ch >= '0' && ch <= '9') return 1;
	else return 0;
}

int isNum(uint8_t str[], int idx){
	if(isDig(str[idx]) && isDig(str[idx+1]) && isDig(str[idx+2]) && isDig(str[idx+3])) return 1;
	else if(isDig(str[idx+1]) && isDig(str[idx+2]) && isDig(str[idx+3])) return 2;
	else if(isDig(str[idx+2]) && isDig(str[idx+3])) return 3;
	else if(isDig(str[idx+3])) return 4;
	else return 0;

}


void cmd_parser_fsm(){
	if(buffer_flag == 1){
		if(buffer_byte == '@'){
			index_buffer = (index_buffer == 0)? 28 : index_buffer-2;
			if(buffer[index_buffer] == 'C'){
				cmd_flag = 1;
				request_check = 0;
			}
			else if (buffer[index_buffer]== 'F'){
				cmd_flag = 0;
				request_check = 0;
			}
			else if (isDig(buffer[index_buffer])){
				if(buffer[index_buffer] == '0'){
					unsigned int temp_time = 10;
					timeChange = temp_time*100;
				}
				else{
					unsigned int temp_time = buffer[index_buffer] - '0';
					timeChange = temp_time*100;
				}
				sig = 1;
				request_check = 0;
			}
			else{
				request_check = 1;
			}

		}
		else{
			request_check = 1;
		}
		request_flag = 1;
		rst_buffer();
		buffer_flag = 0;
	}
}

void cmd_check_request(){
	char str[50];
	if(request_flag == 1){
		request_flag = 0;
		if(request_check == 1){
			HAL_UART_Transmit(&huart2,(void *)str, sprintf(str, "!Request:ERROR#\r\n"), sizeof(str));
		}
		else{
			HAL_UART_Transmit(&huart2,(void *)str, sprintf(str, "!Request:OK#\r\n"), sizeof(str));
		}
	}
}

uint32_t CheckSum(char* arr, uint32_t len_str){
	uint32_t result = 0;
	for(int i=0; i< len_str; i++){
		result += arr[i];
	}
	return result;
}

