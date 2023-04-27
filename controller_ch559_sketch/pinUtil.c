#include "pinUtil.h"
#include "ch446q_driver.h"

void CH552_power(uint8_t on_off){
    if (on_off){
        pinMode(CH552_PMOS_PIN, OUTPUT);
        digitalWrite(CH552_PMOS_PIN, LOW);
    }else{
        pinMode(CH552_PMOS_PIN, INPUT);
        digitalWrite(CH552_PMOS_PIN, LOW);
    }
}

void CH552_enter_bootloader(){
    CH446Q_reset();
    CH552_power(0); //cut power to CH552
    //use CH559_P32 to pull up CH552_P3.6,  CH559_P27 to pull down CH552_P1.5
    delay(CH552_REBOOT_POWEDOWN_TIME);
    pinMode(32, OUTPUT);
    digitalWrite(32, HIGH);
    pinMode(27, LOW);
    digitalWrite(27, LOW);
    CH446Q_switch_channel(CH446_X_CH552_DP_PULLUP, CH446_Y_CH559_P32, true);
    CH446Q_switch_channel(CH446_X_CH552_P15, CH446_Y_CH559_P27, true);
    CH552_power(1); 
}

void CH552_reboot_usercode(){
    CH446Q_reset();
    CH552_power(0); //cut power to CH552
    delay(CH552_REBOOT_POWEDOWN_TIME);
    CH552_power(1); 
}