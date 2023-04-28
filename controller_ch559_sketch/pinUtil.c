#include "pinUtil.h"
#include "ch446q_driver.h"

__code uint8_t validPins[] = {02,03,12,25,26,27,32};

void CH552_power(__data uint8_t on_off){
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

uint8_t checkPinValid(__data uint8_t pin){
    for (__data uint8_t i=0;i<7;i++){
        if (pin == validPins[i]){
            return 1;
        }
    }
    return 0;
}

void restoreAllPins(){
    for (__data uint8_t i=0;i<7;i++){
        restorePin(validPins[i]);
    }
}

void restorePin(__data uint8_t pin){
    if ( (pin == 2) || (pin == 3) ){    //RXD_ TXD_
        return ;
    }else if ( (pin == 26) || (pin == 27) ){  //RXD1 TXD1
        return ;
    }else if ( (pin == 25) ){  //T2EX,PWM2
        digitalRead(25);
    }else if ( (pin == 12) ){  //PWM3
        digitalRead(12);
    }
    return;
}

void disableUART0(){
    //just map it back to non-exising pin, on CH552, Serial0_begin does not affect TX RX as out at least
    PIN_FUNC&=~bUART0_PIN_X; //on CH559, PIN_FUNC|=bUART0_PIN_X will set P0.2/P0.3 to UART0 alone
    TR1 = 0; 
    TI = 0;
    REN = 0;                                                              
    ES = 0;    
}
void disableUART1(){
    SER1_IER = 0;     
    SER1_MCR = 0;
    IE_UART1 = 0;
}

uint8_t readPin(__data uint8_t pin){
    if (checkPinValid(pin)){
        restorePin(pin);
        pinMode(pin, INPUT);
        return digitalRead(pin);
    }else{
        return PIN_ERROR;
    }
}

uint8_t writePin(__data uint8_t pin, __xdata uint8_t value){
    if (checkPinValid(pin)){
        restorePin(pin);
        pinMode(pin, OUTPUT);
        digitalWrite(pin, value);
        return value;
    }else{
        return PIN_ERROR;
    }
}

uint8_t fastPWM3(__data uint8_t value){
    P1_DIR |= bPWM3;    //push pull
    P1_PU |= bPWM3;
    PIN_FUNC &= ~bTMR3_PIN_X;
    T3_CTRL |= bT3_CLR_ALL;   
    T3_CTRL &= ~bT3_CLR_ALL;
    T3_SETUP |= bT3_EN_CK_SE;
    T3_CK_SE_L = (F_CPU/(20000L*255)) & 0xFF;
    T3_CK_SE_H = ((F_CPU/(20000L*255))>>8) & 0xFF;
    T3_SETUP &= ~bT3_EN_CK_SE;
    T3_CTRL |= bT3_OUT_EN;
    T3_END_L = 0xff;
    T3_END_H = 0;
    T3_FIFO_L = value;
    T3_FIFO_H = 0;
    T3_CTRL |= bT3_CNT_EN ;
}
