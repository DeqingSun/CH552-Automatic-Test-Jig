#ifndef __PIN_UTIL_H
#define __PIN_UTIL_H

#include <Arduino.h>

#define CH552_PMOS_PIN 34

void CH552_power(uint8_t on_off);
void CH552_enter_bootloader();

#endif