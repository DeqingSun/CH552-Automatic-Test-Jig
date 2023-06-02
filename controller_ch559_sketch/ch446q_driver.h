#ifndef __CH446Q_DRIVER_H
#define __CH446Q_DRIVER_H

#include <Arduino.h>

#define CH446_RST_PIN 14
#define CH446_DAT_PIN 15
#define CH446_CLK_PIN 17
#define CH446_STB_PIN 16

#define CH446_X_CH552_P30       0
#define CH446_X_CH552_P31       1
#define CH446_X_CH552_RST       2
#define CH446_X_CH552_P17       3
#define CH446_X_CH552_P16       4
#define CH446_X_CH552_P15       5
#define CH446_X_CH552_DP_PULLUP 6
#define CH446_X_CH552_P34       7
#define CH446_X_CH552_P33       8
#define CH446_X_CH552_P11       9
#define CH446_X_EXT_LED_10     10
#define CH446_X_EXT_LED_11     11
#define CH446_X_CH552_P14      12
#define CH446_X_CH552_P32      13
#define CH446_X_CH552_P37      14
#define CH446_X_CH552_P36      15

#define CH446_Y_CH559_P32      0
#define CH446_Y_CH559_P03      1
#define CH446_Y_CH559_P02      2
#define CH446_Y_CH559_P12_RC   3
#define CH446_Y_CH559_P25      4
#define CH446_Y_CH559_P26      5
#define CH446_Y_CH559_P27      6
#define CH446_Y_EXT_PIN_Y7     7

void CH446Q_init();
void CH446Q_reset();
void CH446Q_switch_channel(__data uint8_t x, __xdata uint8_t y, __xdata uint8_t status);
void CH446Q_save_matrix();
void CH446Q_restore_matrix();

#endif