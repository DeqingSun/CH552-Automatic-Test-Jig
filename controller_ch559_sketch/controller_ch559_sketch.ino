
#ifndef USER_USB_RAM
#error "This example needs to be compiled with a USER USB setting"
#endif

#include "src/userUsbCdc/USBCDC.h"

void setup() {
  USBInit();
}

void loop() {

  USBSerial_print("ECHO:");
  USBSerial_println();
  USBSerial_flush();
  delay(1000);

}
