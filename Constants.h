#ifndef CONSTANTS_H
#define CONSTANTS_H

#define GLITCH                      100

/* queue state machine */
#define QUEUE_GO                    0
#define QUEUE_STOP                  1
#define QUEUE_READY_CUP             2

/* main state machine */
#define ONLY_WAITING                0
#define RESET                       1
#define RESET_QUEUE                 2   
#define RESET_SERVO                 3
#define RESET_HORIZONTAL_INTERRUPT  4   
#define RESET_HORIZONTAL_DEFAULT    5 
#define RESET_VERTICAL_DEFAULT      6
#define STARTING                    7
#define VERTICAL_HOLD_CUP           8
#define VERTICAL_REMOVE_LID_HOLDER  9
#define HORIZONTAL_HOLD_HOLDER      10
#define HORIZONTAL_PLACE_HOLDER     11
#define HORIZONTAL_HOLD_CUP         12
#define HORIZONTAL_WASTE_CUP        13
#define HORIZONTAL_WASH_CUP         14
#define HORIZONTAL_LOAD_CUP         15

/* pin num definition */
const int LOADCELL_DATA_PIN                 = 35;
const int LOADCELL_CLK_PIN                  = 36;

const int RESET_PIN                         = 2;
const int QUEUE_DOOR_PIN                    = 3;

const int WATERPUMP_EN                      = 4;
const int WATERPUMP_PIN_1                   = 5;
const int WATERPUMP_PIN_2                   = 6;

const int QUEUE_STEPPER_PUL                 = 38;
const int QUEUE_STEPPER_DIR                 = 39;
const int QUEUE_STEPPER_ENA                 = 37;

const int HORIZONTAL_STEPPER_wrist_pin      = 22;
const int HORIZONTAL_STEPPER_finger_pin     = 23;
const int VERTICAL_STEPPER_finger_pin       = 18;

const int small_cup_servo_pin               = 13;
const int regular_cup_servo_pin             = 12;
const int large_cup_servo_pin               = 11;
const int remove_lid_servo_pin              = 17;

const int VERTICAL_STEPPER_reset_pin        = 19;
const int HORIZONTAL_STEPPER_reset_pin      = 20;
const int QUEUE_INTERRUPT_PIN               = 21;

const int ECHO_PIN = 45;
const int TRIG_PIN = 47;

// vertical, horizontal stepper motor speed 
// Steps Per Revolution (회전 당 스텝 수) definition
const int VERTICAL_STEPPER_SPEED            = 300;
const int HORIZONTAL_STEPPER_SPEED          = 300;
const int SPR                               = 200;
const int microStepping                     = 32;

/* stepper motor constants definition */
const int VERTICAL_STEPPER_DELAY            = ((60L * 1000L * 1000 / SPR / VERTICAL_STEPPER_SPEED) + 50);
const int HORIZONTAL_STEPPER_DELAY          = ((60L * 1000L * 1000 / SPR / HORIZONTAL_STEPPER_SPEED) + 50);
const float pi = 3.14;
const float CmPerCycle = 4.71;

/* position definition */
const float horizontal_pos_default          = 42.5;
const float horizontal_pos_reset            = 2.5;
const float horizontal_pos_wash             = 14;
const float horizontal_pos_waste            = 24;

const float vertical_pos_default            = 0;
const float vertical_pos_remove_lid         = 5;
const float vertical_pos_remove_holder      = 6;
const float vertical_pos_holder             = 12;
const float vertical_pos_cup                = 12;

const int left  = -1;
const int right = 1;
const int up    = 1;
const int down  = -1;

/* horizontal servo motor angle definition */
const int HORIZONTAL_STEPPER_finger_default = 120;
const int HORIZONTAL_STEPPER_wrist_default  = 170;
const int HORIZONTAL_STEPPER_wrist_load     = 45;

const int HORIZONTAL_STEPPER_finger_holder  = 60;
const int HORIZONTAL_STEPPER_finger_cup     = 44;
const int HORIZONTAL_STEPPER_wrist_waste    = 45;
const int HORIZONTAL_STEPPER_wrist_wash     = 65;

/* vertical servo motor angle definition */
const int VERTICAL_STEPPER_finger_minimum   = 40;
const int VERTICAL_STEPPER_finger_default   = 155;
 
/* cup cnt threshold */
const int small_cnt_threshold               = 1;
const int regular_cnt_threshold             = 1;
const int large_cnt_threshold               = 1;

const int cleaning_cup_angle                = 180;
const int default_cup_angle                 = 0;

/* actuator delay for removing lid */   
const int REMOVE_LID_ANGLE[7]               = {170, 80, 123, 135, 80, 123, 135};
const float horizontal_pos_cup_size[7]      = {0, 96.5, 82, 63, 96.5, 82, 63};

/* finger angle */
const int HORIZONTAL_STEPPER_finger_ready_cup[7] = {0, 63, 66, 70, 63, 66, 70};
const int VERTICAL_STEPPER_finger_remove_lid[7]  = {0, 40, 40, 90, 40, 40, 90};
const int VERTICAL_STEPPER_finger_cup[7]         = {0, 60, 70, 85, 60, 70, 85};
const int VERTICAL_STEPPER_finger_ready_cup[7]   = {0, 75, 95, 120, 75, 95, 120};


#endif