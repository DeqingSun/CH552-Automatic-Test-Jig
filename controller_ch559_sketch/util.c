#include "util.h"

uint8_t hexToUchar(char s) {
  if (s >= '0' && s <= '9') {
    return (s - '0');
  }
  if (s >= 'A' && s <= 'F')  {
    return (s - 'A' + 10);
  }
  if (s >= 'a' && s <= 'f') {
    return (s - 'a' + 10);
  }
  return 0xff;
}

uint8_t hexToUchar2_xdata(__xdata char * __data s) {
  return (hexToUchar(*s) << 4) + hexToUchar(*(s + 1));
}

uint16_t hexToUint16_xdata(__xdata char * __data s) {
  return (hexToUchar2_xdata(s) << 8) + hexToUchar2_xdata(s + 2);
}