from pynput import keyboard, mouse
from ch559_jig_code import CH559_jig
import time

keyboard_mouse_input = ""

def on_press(key):
    global keyboard_mouse_input
    try:
        keyboard_mouse_input = keyboard_mouse_input+(key.char)
        print(keyboard_mouse_input)
    except AttributeError:
        pass

def on_move(x, y):
    global keyboard_mouse_input
    keyboard_mouse_input = keyboard_mouse_input+"Moved"
    print(keyboard_mouse_input)

def on_click(x, y, button, pressed):
    global keyboard_mouse_input
    if (pressed):
        keyboard_mouse_input = keyboard_mouse_input+"Pressed"
        print(keyboard_mouse_input)

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

pins_and_outputs = [[ch559_jig.PIN_CH552_P30_X,"a"],[ch559_jig.PIN_CH552_P31_X,"Pressed"],[ch559_jig.PIN_CH552_P32_X,"Moved"]]

ch559_jig.digital_write(25,True)

time.sleep(0.1)

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()
mouse_listener = mouse.Listener(on_move=on_move,on_click=on_click,)
mouse_listener.start()

for pin_and_output in pins_and_outputs:
    pin = pin_and_output[0]
    output = pin_and_output[1]
    ch559_jig.connect_pins(pin,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
    time.sleep(0.1)
    keyboard_mouse_input = ""
    ch559_jig.digital_write(25,False)
    time.sleep(0.1)
    ch559_jig.digital_write(25,True)
    time.sleep(0.1)
    #if keyboard_mouse_input contains output
    if (keyboard_mouse_input.find(output)<0):
        print(f"CH559 keyboard input {keyboard_mouse_input} not match output {output}")
        exit(1)

    ch559_jig.disconnect_pins(pin,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)
