#ifndef __UTIL_H
#define __UTIL_H

#include <Arduino.h>

uint8_t hexToUchar(__data char s);
uint8_t hexToUchar2_xdata(__xdata char * __data s);
uint16_t hexToUint16_xdata(__xdata char * __data s);

#endif
