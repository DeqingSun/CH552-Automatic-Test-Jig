#include "ch446q_driver.h"

__xdata uint8_t currentMatrixStatus[16] = {0};  //16 X channels and 8 Y channels. 
__xdata uint8_t savedtMatrixStatus[16] = {0};  

void CH446Q_init() {
  digitalWrite(CH446_RST_PIN, LOW);
  pinMode(CH446_RST_PIN, OUTPUT);

  digitalWrite(CH446_DAT_PIN, LOW);
  pinMode(CH446_DAT_PIN, OUTPUT);

  digitalWrite(CH446_CLK_PIN, LOW);
  pinMode(CH446_CLK_PIN, OUTPUT);

  digitalWrite(CH446_STB_PIN, LOW);
  pinMode(CH446_STB_PIN, OUTPUT);
}

void CH446Q_reset() {
  digitalWrite(CH446_RST_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(CH446_RST_PIN, LOW);

  for (__data uint8_t i = 0; i < 16; i++) {
    currentMatrixStatus[i] = 0;
  }
}

void CH446Q_switch_channel(__data uint8_t x, __xdata uint8_t y, __xdata uint8_t status) {
  //output y
  for (__data int8_t i = 2; i >= 0; i--) {
    digitalWrite(CH446_CLK_PIN, LOW);
    digitalWrite(CH446_DAT_PIN, (y >> i) & 0x01);
    delayMicroseconds(1);
    digitalWrite(CH446_CLK_PIN, HIGH);
    delayMicroseconds(1);
  }

  //output x
  for (__data int8_t i = 3; i >= 0; i--) {
    digitalWrite(CH446_CLK_PIN, LOW);
    digitalWrite(CH446_DAT_PIN, (x >> i) & 0x01);
    delayMicroseconds(1);
    digitalWrite(CH446_CLK_PIN, HIGH);
    delayMicroseconds(1);
  }

  //output ON
  digitalWrite(CH446_DAT_PIN, HIGH);
  delayMicroseconds(1);
  if (status) {
    digitalWrite(CH446_STB_PIN, HIGH);
    delayMicroseconds(1);
    digitalWrite(CH446_STB_PIN, LOW);
    currentMatrixStatus[x] |= 1<<y;
  }
  delayMicroseconds(1);

  //output OFF
  digitalWrite(CH446_DAT_PIN, LOW);
  delayMicroseconds(1);
  if (!status) {
    digitalWrite(CH446_STB_PIN, HIGH);
    delayMicroseconds(1);
    digitalWrite(CH446_STB_PIN, LOW);
    currentMatrixStatus[x] &= ~(1<<y);
  }
  delayMicroseconds(1);

  digitalWrite(CH446_CLK_PIN, LOW);
  digitalWrite(CH446_DAT_PIN, HIGH);
}

void CH446Q_save_matrix(){
  for (__data uint8_t i=0;i<16;i++){
    savedtMatrixStatus[i] = currentMatrixStatus[i];
    //USBSerial_println(currentMatrixStatus[i],HEX);
  }
}

void CH446Q_restore_matrix(){
  for (__data uint8_t i=0;i<16;i++){
    if ( savedtMatrixStatus[i] == currentMatrixStatus[i] ){
      continue;
    }
    for (__data uint8_t j=0;j<8;j++){
      if ((savedtMatrixStatus[i] & (1<<j)) != (currentMatrixStatus[i] & (1<<j))){
        if (savedtMatrixStatus[i] & (1<<j)){
          CH446Q_switch_channel(i,j,true);
        }else{
          CH446Q_switch_channel(i,j,false);
        }
      }
    }
  }
}