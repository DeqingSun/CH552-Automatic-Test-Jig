# CH552 Automatic Test Jig

This project does regression test on hardware for [Ch55xduino](https://github.com/DeqingSun/ch55xduino). It automatically compiles a batch of Arduino sketches, uploads the hex files into a target CH552 chip, and checks the behavior of the firmware with test scripts. 

![photo of circuit board with raspberry pi](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/board_photo.jpg)

## Why I made this

Most regression tests are limited to the software level. For most of the continuous integration setup for the Arduino projects, as far as I know. They only compile the sketches in a virtual machine and see if the compilation goes through. The SDCC compiler project goes one step further. The SDCC uses a simulator to verify code on different MCU architectures. However, when the regression tests involve peripherals, especially USB, there will be no good way to do simulation. Doing regression tests on real hardware will be necessary.

## How does it work

A raspberry pi computer runs a script to compile every Arduino example of CH55xduino. For each of the Arduino examples, the pi connects to a test jig board to restart the target CH552 chip into bootloader mode and upload the compiled hex file. Then the pi will use the corresponding test script to test the behavior of the hex file, with the CH559 and switch matrix chip on the test jig board. 

The CH559 can do digital/analog read/write to the target CH552 chip. The pi can do the USB communication. Then the raspberry pi will be able to test if the hex works in a way matches the defination in the test script. 

## Hardware

The circuit board of the test jig contains a CH559 chip that acts as a controller to do digital IO, serial communication, and makeshift analog IO with a T filter. The CH552 chip is mounted in an SMT Test Socket because the chip has low flash write cycles. The CH446Q switch matrix chip connects any CH552 pin to any CH559 function pin with great flexibility. Also, the CH559 can power cycle the CH552 chip with a MOSFET. So the CH552 can enter bootload mode safely.    

The Raspberry Pi serves as the compiler and controller of the whole system. Raspberry Pi uses a USB cable to control the CH559 chip and another USB cable to control the target CH552 chip.

## Software

The software part is a bunch of Python scripts. At this moment, the software is not connected to continuous integration because of security concerns and 14 days limit of Github Action self-hosted runner. 

The master test script uses Arduino Cli tool to compile all examples into hex files and check if there is any failure. Then for each of the hex file, the master test script will power cycle the target chip and upload the hex file, then pull the the matching sketch test script to validate the funtions.

Also, another script exposes the CH559 chip to a webpage. And it is easier to use the board for general development and debugging, especially when the board when is used remotely.

![photo of control webpage](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/control_page.png)

