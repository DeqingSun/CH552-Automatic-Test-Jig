import time

from ch559_jig_code import CH559_jig
from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()
ch559_jig = CH559_jig()

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.digital_write(25, True, wait_for_input_time=1)
ch552_state = 1 # 1 at beginning
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P32, wait_for_input_time=1)
time.sleep(0.1)
ch552_serial_code.check_input() # clear input

test_digital_values = [False, True, False, True, False, True]
for test_digital_value in test_digital_values:
    led_value = ch559_jig.digital_read(32, wait_for_input_time=1)
    if (led_value != False):
        print(f"CH552 LED On on mistake")
        exit(1)
    ch559_jig.digital_write(25, test_digital_value, wait_for_input_time=1)
    time.sleep(0.1)
    return_list = ch552_serial_code.check_input()
    if (not test_digital_value):
        if (len(return_list) != 1 or return_list[0] != "off"):
            print(f"CH552 serial not expected off")
            exit(1)
    else:
        if (len(return_list) != 2 or return_list[0] != "on"):
            print(f"CH552 serial not expected on")
            exit(1)
        res = [int(i) for i in return_list[1].split() if i.isdigit()]
        ch552_state+=1
        if (ch552_state != res[0]):
            print(f"CH552 serial not expected state {ch552_state} {res[0]}")
            exit(1)
        if (ch552_state == 4):
            led_value = ch559_jig.digital_read(32, wait_for_input_time=1)
            if (led_value != True):
                print(f"CH552 LED Off on mistake")
                exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)