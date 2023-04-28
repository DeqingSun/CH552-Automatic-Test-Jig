//compiled with CH559, CH55xduino 0.0.17
//userUsbCdc used for customized description

#ifndef USER_USB_RAM
#error "This example needs to be compiled with a USER USB setting"
#endif

#include "src/userUsbCdc/USBCDC.h"
#include "ch446q_driver.h"
#include "pinUtil.h"
#include "util.h"

char rxSerialBuffer[16];
uint8_t rxSerialBufferPtr = 0;
uint8_t digitalPinSubscribed = 255;
uint32_t digitalPinSubscribedLastPrintTime = 0;

void setup() {
  CH552_power(true);

  USBInit();
  CH446Q_init();
  CH446Q_reset();

  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);
  CH446Q_switch_channel(9, 3, true);
  CH446Q_switch_channel(7, 4, true);

//  analogWrite(25, 64);
//CH552_enter_bootloader();
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
          case 'I':
            if (rxSerialBufferPtr == 1) {
              USBSerial_println("I:Init System");
              CH446Q_reset();
              digitalPinSubscribed = 255;
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
                USBSerial_print(":Turn ");
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
          case 'B':
            if (rxSerialBufferPtr == 1) {
              USBSerial_println("B: CH552 boot mode");
              CH552_enter_bootloader();
            }
            break;
          case 'b':
            if (rxSerialBufferPtr == 1) {
              USBSerial_println("b: CH552 reboot usercode");
              CH552_reboot_usercode();
            }
            break;
          case 'R':
          case 'r':
            if (rxSerialBufferPtr == 3) {
              uint8_t pinChannel = hexToUchar(rxSerialBuffer[1]);
              uint8_t pinNumber = hexToUchar(rxSerialBuffer[2]);
              uint8_t pinStatus = readPin(pinChannel*10+pinNumber);
              USBSerial_print(rxSerialBuffer[0]);
              USBSerial_print(rxSerialBuffer[1]);
              USBSerial_print(rxSerialBuffer[2]);
              USBSerial_print((char)':');
              if (pinStatus==PIN_ERROR){
                USBSerial_println("not valid");
              }else{
                USBSerial_println((char)('0'+pinStatus));
                if (rxSerialBuffer[0] == 'R') {
                  digitalPinSubscribed = 255;
                }else{
                  digitalPinSubscribed = pinChannel*10+pinNumber;
                  digitalPinSubscribedLastPrintTime = millis();
                }
              }
            }
            break;
          
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

  if (digitalPinSubscribed!=255){
    if (((int)(millis()-digitalPinSubscribedLastPrintTime))>25){
      uint8_t pinStatus = readPin(digitalPinSubscribed);
      USBSerial_print((char)'r');
      if (pinStatus<0){
        USBSerial_print((char)'0');
      }
      USBSerial_print((int)digitalPinSubscribed);
      USBSerial_print((char)':');
      USBSerial_println((char)('0'+pinStatus));
      digitalPinSubscribedLastPrintTime = millis();
    }
  }


//analogWrite(12,64);
  //analogWrite(25, 64);
 // CH552_POWER(true);
 // CH446Q_reset();
//delay(2000);
//digitalWrite(12,128);
  //digitalWrite(25, LOW);
 // CH552_POWER(false);
 // CH446Q_reset();
 // delay(2000);

  /*CH446Q_switch_channel(10,7,false);
    CH446Q_switch_channel(11,7,true);
    delay(3000);
    CH446Q_switch_channel(10,7,true);
    CH446Q_switch_channel(11,7,false);
    delay(3000);*/

  /*CH552_enter_bootloader();
    delay(10000);
    CH446Q_reset();
    CH552_power(0); 
    delay(10);
    CH552_power(1); 
    delay(10000);*/
}

