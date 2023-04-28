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
uint8_t analogPinSubscribed = 255;
uint32_t digitalPinSubscribedLastPrintTime = 0;
uint32_t analogPinSubscribedLastPrintTime = 0;

void setup() {
  CH552_power(true);

  USBInit();
  CH446Q_init();
  CH446Q_reset();
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
              restoreAllPins();
              digitalPinSubscribed = 255;
              analogPinSubscribed = 255;
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
              uint8_t pin = hexToUchar(rxSerialBuffer[1])*10+hexToUchar(rxSerialBuffer[2]);
              uint8_t pinStatus = readPin(pin);
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
                  digitalPinSubscribed = pin;
                  digitalPinSubscribedLastPrintTime = millis();
                }
              }
            }
            break;
          case 'A':
          case 'a':
            if (rxSerialBufferPtr == 3) {
              uint8_t pin = hexToUchar(rxSerialBuffer[1])*10+hexToUchar(rxSerialBuffer[2]);
              USBSerial_print(rxSerialBuffer[0]);
              USBSerial_print(rxSerialBuffer[1]);
              USBSerial_print(rxSerialBuffer[2]);
              USBSerial_print((char)':');
              if (pin!=12){
                USBSerial_println("not valid");
              }else{
                USBSerial_println(analogRead(pin));
                if (rxSerialBuffer[0] == 'A') {
                  analogPinSubscribed = 255;
                }else{
                  analogPinSubscribed = pin;
                  analogPinSubscribedLastPrintTime = millis();
                }
              }
            }
            break;
          case 'W':
            if (rxSerialBufferPtr == 4) {
              uint8_t pin = hexToUchar(rxSerialBuffer[1])*10+hexToUchar(rxSerialBuffer[2]);
              uint8_t value = hexToUchar(rxSerialBuffer[3]);
              USBSerial_print(rxSerialBuffer[0]);
              USBSerial_print(rxSerialBuffer[1]);
              USBSerial_print(rxSerialBuffer[2]);
              USBSerial_print((char)':');
              
              uint8_t pinStatus = writePin(pin,value);
              if (pinStatus==PIN_ERROR){
                USBSerial_println("not valid");
              }else{
                USBSerial_println((char)('0'+pinStatus));
              }
            }
            break;
          case 'w':
            if (rxSerialBufferPtr == 5) {
              uint8_t pin = hexToUchar(rxSerialBuffer[1])*10+hexToUchar(rxSerialBuffer[2]);
              uint8_t value = hexToUchar2_xdata(&rxSerialBuffer[3]);
              USBSerial_print(rxSerialBuffer[0]);
              USBSerial_print(rxSerialBuffer[1]);
              USBSerial_print(rxSerialBuffer[2]);
              USBSerial_print((char)':');
              if ( (pin==12) || (pin==25) ){
                if (pin==25){
                  analogWrite(25, value); //just default 1K for P25
                }else{
                  fastPWM3(value);  //20K for P12
                }
                USBSerial_print((int)value);
              }else{
                USBSerial_println("not valid");
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

  //repeat output of digital pin status if subscribed
  if (digitalPinSubscribed!=255){
    if (((int)(millis()-digitalPinSubscribedLastPrintTime))>25){
      uint8_t pinStatus = readPin(digitalPinSubscribed);
      USBSerial_print((char)'r');
      if (digitalPinSubscribed<10){
        USBSerial_print((char)'0');
      }
      USBSerial_print((int)digitalPinSubscribed);
      USBSerial_print((char)':');
      USBSerial_println((char)('0'+pinStatus));
      digitalPinSubscribedLastPrintTime = millis();
    }
  }
  //repeat output of analog pin status if subscribed
  if (analogPinSubscribed!=255){
    if (((int)(millis()-analogPinSubscribedLastPrintTime))>25){
      USBSerial_print((char)'a');
      if (analogPinSubscribed<10){
        USBSerial_print((char)'0');
      }
      USBSerial_print((int)analogPinSubscribed);
      USBSerial_print((char)':');
      USBSerial_println(analogRead(analogPinSubscribed));
      analogPinSubscribedLastPrintTime = millis();
    }
  }
  
}

