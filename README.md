# CH552 Automatic Test Jig

This project does regression test on hardware for [Ch55xduino](https://github.com/DeqingSun/ch55xduino). It automatically compiles a batch of Arduino sketches, uploads the hex files into a target CH552 chip, and checks the behavior of the firmware with test scripts. 

![photo of circuit board with raspberry pi](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/board_photo.jpg)

## Why I made this

Most regression tests are limited to the software level. For most of the continuous integration setup for the Arduino projects, as far as I know. They only compile the sketches in a virtual machine and see if the compilation goes through. The SDCC compiler project goes one step further. The SDCC uses a simulator to verify code on different MCU architectures. However, when the regression tests involve peripherals, especially USB, there will be no good way to do simulation. Doing regression tests on real hardware will be necessary.

## How does it work

A raspberry pi computer runs a script to compile every Arduino example of CH55xduino. For each of the Arduino examples, the pi connects to a test jig board to restart the target CH552 chip into bootloader mode and upload the compiled hex file. Then the pi will use the corresponding test script to test the behavior of the hex file, with the CH559 and switch matrix chip on the test jig board. 

The CH559 can do digital/analog read/write to the target CH552 chip. The pi can do the USB communication. Then the raspberry pi will be able to test if the hex works in a way matches the defination in the test script. 

## Hardware

## Software

