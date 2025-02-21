#ifndef CONFIG_H
#define CONFIG_H

volatile int reset_horizontal_direct;

float current_horizontal_pos;
float current_vertical_pos;

float next_horizontal_pos;
float next_vertical_pos;

int horizontal_pos_cup;

int cup_size, cup_size_entrance, holder_exist;
int cup_cnt[5];

volatile int main_current_state = RESET;
volatile int queue_current_state = QUEUE_READY_CUP;

volatile int main_last_state;
volatile int queue_last_state;

int current_cup_size = 0;
int current_entrance_size = 0;
int current_holder_exist = 0;

int next_cup_size = 0;
int next_entrance_size = 0;
int next_holder_exist = 0;

int getByte;

volatile int end_time = 0, start_time = 0;
volatile int reset_flag = 0;

int          queue_mode = 0; // 0 : interrupt, other : step
volatile int queue_flag = 0; // 0 : stop, 1 : run

volatile int all_stop = 0;

byte tx_rx_data = 0;

unsigned char cup_queue[3] = {0, 0, 0};

#endif