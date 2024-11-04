# CH552 Automatic Test Jig

This project does regression test on hardware for [Ch55xduino](https://github.com/DeqingSun/ch55xduino). It automatically compiles a batch of Arduino sketches, uploads the hex files into a target CH552 chip, and checks the behavior of the firmware with test scripts. This tool can also be integrated into [GitHub action](https://github.com/DeqingSun/ch55xduino/blob/ch55xduino/.github/workflows/checkSketches.yml) for automatic testing.

![photo of circuit board with raspberry pi](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/board_photo.jpg)

## Why I made this

Most regression tests are limited to the software level. For most of the continuous integration setup for the Arduino projects, as far as I know. They only compile the sketches in a virtual machine and see if the compilation goes through. The SDCC compiler project goes one step further. The SDCC uses a simulator to verify code on different MCU architectures. However, when the regression tests involve peripherals, especially USB, there will be no good way to do simulation. Doing regression tests on real hardware will be necessary.

## How does it work

A raspberry pi computer runs a script to compile every Arduino example of CH55xduino. For each of the Arduino examples, the pi connects to a test jig board to restart the target CH552 chip into bootloader mode and upload the compiled hex file. Then the pi will use the corresponding test script to test the behavior of the hex file, with the CH559 and switch matrix chip on the test jig board. 

The CH559 can do digital/analog read/write to the target CH552 chip. The pi can do the USB communication. Then the raspberry pi will be able to test if the hex works in a way matches the defination in the test script. 

Let's use [Blink](https://github.com/DeqingSun/ch55xduino/blob/ch55xduino/ch55xduino/ch55x/libraries/Generic_Examples/examples/01.Basics/Blink/Blink.ino) as an example. First CH559 will reset the multiplexer, and cut the power of target CH552 with a P-Mos. Then the CH559 will use a multiplexer to connect P3.6(D+) of CH552 to CH559's GPIO with 3.3V output and connect P1.5 of CH552 to CH559's GPIO with 0V output. Then the power of CH552 is restored. No matter which pin is used in the Bootloader entry is used, the CH552 will always enter the bootloader mode. Then the Raspberry Pi uses the [vnproch551](https://github.com/DeqingSun/vnproch551/tree/master) tool to upload the Blink.ino.hex to CH552. After that, the P3.3 of CH552 will toggle every second. The Raspberry Pi will execute the [jig_test_Blink.py](https://github.com/DeqingSun/CH552-Automatic-Test-Jig/blob/main/python/sketchTestCode/jig_test_Blink.py) tool to use a multiplexer to connect P3.3 of CH552 to P2.5 of CH559, and also connect that P2.5 of CH559 to the onboard LED so the blinking will be visible. If the P2.5 of CH559 gets 2 toggles and the timing is between 0.95 and 1.05 seconds, the test is considered successful. 

## Hardware

The [circuit board](https://github.com/DeqingSun/CH552-Automatic-Test-Jig/blob/main/PCB/CH552_autoTest_v2.pdf) of the test jig contains a CH559 chip that acts as a controller to do digital IO, serial communication, and makeshift analog IO with a T filter. The CH552 chip is mounted in an SMT Test Socket because the chip has low flash write cycles. The CH446Q switch matrix chip connects any CH552 pin to any CH559 function pin with great flexibility. Also, the CH559 can power cycle the CH552 chip with a MOSFET. So the CH552 can enter bootload mode safely.

There are also 3 on board LEDs, the red one indicates the power status of the CH552, and the 2 white LEDs can be mapped to any CH559 pins for visual indication. Also, there are 3 switch matrix pins exposed as pin headers so additional programmer or test instruments can be connected.

The Raspberry Pi serves as the compiler and controller of the whole system. Raspberry Pi uses a USB cable to control the CH559 chip and another USB cable to control the target CH552 chip.

## Software

The software part is a bunch of Python scripts. It can be used as standalone project or connected to Github Action.

The master test script uses Arduino Cli tool to compile all examples into hex files and check if there is any failure. Then for each of the hex file, the master test script will power cycle the target chip and upload the hex file, then pull the the matching sketch test script to validate the funtions.

Also, another script exposes the CH559 chip to a webpage. And it is easier to use the board for general development and debugging, especially when the board when is used remotely.

![photo of control webpage](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/control_page.png)

## Integration of Github Action

![Github Action flow](https://raw.githubusercontent.com/DeqingSun/CH552-Automatic-Test-Jig/main/img/github_action_flow.png)

The [CH55xduino project](https://github.com/DeqingSun/ch55xduino) uses this project for automatic testing. As a public repo, CH55xduino has access to free GitHub-hosted runners. So the CH55xduino utilizes the GitHub-hosted runners to do clang-format checks and Arduino code compilation on the cloud with Arduino Cli to verify if all examples can be compiled successfully on each GitHub push. Then all compiled hex files are packed and uploaded as artifacts. Then the self-hosted runner on Raspberry Pi will take over the artifacts from cloud runner to bypass all Arduino compilation steps and use [selfhost_runner_test.py](https://github.com/DeqingSun/CH552-Automatic-Test-Jig/blob/main/python/selfhost_runner_test.py) to test all hex files one by one, to verify if all hex files behave the same way as defined in the test scripts. If every test passes successfully, the whole repo should work well.
