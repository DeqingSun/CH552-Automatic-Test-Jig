#ifndef __PIN_UTIL_H
#define __PIN_UTIL_H

#include <Arduino.h>

#define CH552_PMOS_PIN 34
#define CH552_REBOOT_POWEDOWN_TIME 30

#define PIN_ERROR 255

void CH552_power(__data uint8_t on_off);
void CH552_enter_bootloader();
void CH552_reboot_usercode();

uint8_t checkPinValid(__data uint8_t pin);
void restoreAllPins();
void restorePin(__data uint8_t pin);
void disableUART0();
void disableUART1();
uint8_t readPin(__data uint8_t pin);
uint8_t writePin(__data uint8_t pin, __xdata uint8_t value);
uint8_t fastPWM3(__data uint8_t value);

#endif