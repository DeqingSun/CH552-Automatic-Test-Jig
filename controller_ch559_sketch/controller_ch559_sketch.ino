//compiled with CH559, CH55xduino 0.0.17
//userUsbCdc used for customized description

#ifndef USER_USB_RAM
#error "This example needs to be compiled with a USER USB setting"
#endif

#include "src/userUsbCdc/USBCDC.h"
#include "ch446q_driver.h"
#include "util.h"

char rxSerialBuffer[16];
uint8_t rxSerialBufferPtr = 0;

void setup() {
  USBInit();
  CH446Q_init();
  CH446Q_reset();

  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);
  CH446Q_switch_channel(9, 3, true);
  CH446Q_switch_channel(7, 4, true);

  analogWrite(25, 64);

  //delay(100);
  //CH446Q_reset();
  
}

void loop() {

  while (USBSerial_available()) {
    char serialChar = USBSerial_read();
    if ((serialChar == '\n') || (serialChar == '\r') ) {
      rxSerialBuffer[rxSerialBufferPtr] = '\0';
      if (rxSerialBufferPtr > 0) {
        //USBSerial_println(rxSerialBuffer);
        switch (rxSerialBuffer[0])
        {
          case 'R':
            if (rxSerialBufferPtr == 1) {
              USBSerial_println("R: Reset System");
              CH446Q_reset();
            }
            break;
          case 'C':
          case 'c':
            //connect channels on CH446Q
            if (rxSerialBufferPtr == 3) {
              uint8_t xChannel = hexToUchar(rxSerialBuffer[1]);
              uint8_t yChannel = hexToUchar(rxSerialBuffer[2]);
              uint8_t onOFF = (rxSerialBuffer[0] == 'C') ? 1 : 0;

              if ( (xChannel < 16) && (yChannel < 8)) {
                USBSerial_print(rxSerialBuffer[0]);
                USBSerial_print(": Turn ");
                if (onOFF == 1) {
                  USBSerial_print("ON");
                } else {
                  USBSerial_print("OFF");
                }
                USBSerial_print(" X:");
                USBSerial_print(xChannel);
                USBSerial_print(", Y:");
                USBSerial_println(yChannel);
                CH446Q_switch_channel(xChannel, yChannel, onOFF);
              }

            }
          default:
            break;
        }
        rxSerialBufferPtr = 0;
        break;
      }
    } else {
      if (rxSerialBufferPtr < (16 - 1)) {
        rxSerialBuffer[rxSerialBufferPtr] = serialChar;
        rxSerialBufferPtr++;
      } else {
        rxSerialBuffer[rxSerialBufferPtr] = '\0';
      }
    }
  }


  USBSerial_flush();

analogWrite(12,64);
  analogWrite(25, 64);
delay(100);
digitalWrite(12,128);
  digitalWrite(25, LOW);
  delay(100);

  /*CH446Q_switch_channel(10,7,false);
    CH446Q_switch_channel(11,7,true);
    delay(3000);
    CH446Q_switch_channel(10,7,true);
    CH446Q_switch_channel(11,7,false);
    delay(3000);*/
}
