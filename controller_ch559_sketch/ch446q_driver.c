#include "ch446q_driver.h"

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
  }
  delayMicroseconds(1);

  //output OFF
  digitalWrite(CH446_DAT_PIN, LOW);
  delayMicroseconds(1);
  if (!status) {
    digitalWrite(CH446_STB_PIN, HIGH);
    delayMicroseconds(1);
    digitalWrite(CH446_STB_PIN, LOW);
  }
  delayMicroseconds(1);

  digitalWrite(CH446_CLK_PIN, LOW);
  digitalWrite(CH446_DAT_PIN, HIGH);
}
