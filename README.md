# CH552 Automatic Test Jig

This project does regression test on hardware for [Ch55xduino](https://github.com/DeqingSun/ch55xduino). It automatically compiles a batch of Arduino sketches, uploads the hex files into a target CH552 chip, and checks the behavior of the firmware with test scripts. 

![photo of circuit board with raspberry pi](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/board_photo.jpg)

## Why I made this

Most regression tests are limited to the software level. For most of the continuous integration setup for the Arduino projects, as far as I know. They only compile the sketches in a virtual machine and see if the compilation goes through. The SDCC compiler project goes one step further. The SDCC uses a simulator to verify code on different MCU architectures. However, when the regression tests involve peripherals, especially USB, there will be no good way to do simulation. Doing regression tests on real hardware will be necessary.

## How does it work

## Hardware

## Software

