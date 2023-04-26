#ifndef __CH446Q_DRIVER_H
#define __CH446Q_DRIVER_H

#include <Arduino.h>

#define CH446_RST_PIN 14
#define CH446_DAT_PIN 15
#define CH446_CLK_PIN 17
#define CH446_STB_PIN 16

void CH446Q_init();

void CH446Q_reset();

void CH446Q_switch_channel(__data uint8_t x, __xdata uint8_t y, __xdata uint8_t status);

#endif