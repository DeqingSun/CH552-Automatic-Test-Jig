//compiled with CH559, CH55xduino 0.0.17
//userUsbCdc used for customized description

#ifndef USER_USB_RAM
#error "This example needs to be compiled with a USER USB setting"
#endif

#include "src/userUsbCdc/USBCDC.h"
#include "ch446q_driver.h"

void setup() {
  USBInit();
  CH446Q_init();
  CH446Q_reset();
}

void loop() {

  USBSerial_print("ECHO!!!:");
  USBSerial_println();
  USBSerial_flush();

  
  CH446Q_switch_channel(10,7,false);
  delay(3000);
  CH446Q_switch_channel(10,7,true);
  delay(3000);
}
