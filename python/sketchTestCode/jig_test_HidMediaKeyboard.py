from pynput import keyboard
from ch559_jig_code import CH559_jig
import time

keyboard_input = ""

def on_press(key):
    global keyboard_input
    try:
        keyboard_input = keyboard_input+(key.char)
    except AttributeError:
        keyboard_input ='special key {0} pressed'.format(key)

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.digital_write(25,True)

time.sleep(0.1)

listener = keyboard.Listener(on_press=on_press)
listener.start()

output = "Key.media_volume_up"

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
time.sleep(0.1)
keyboard_input = ""
ch559_jig.digital_write(25,False)
time.sleep(0.1)
ch559_jig.digital_write(25,True)
time.sleep(0.1)
if (keyboard_input.find(output)<0):
    print(f"CH559 keyboard input {keyboard_input} not match output {output}")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)
