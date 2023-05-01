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

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)

test_digital_values = [False, True, False, True, False, True]
for test_digital_value in test_digital_values:
    ch559_jig.digital_write(25, test_digital_value, wait_for_input_time=1)
    time.sleep(0.1)
    return_list = ch552_serial_code.check_input()
    if (len(return_list) == 0):
        print("CH552 serial no input")
        exit(1)
    last_return_string = return_list[-1].strip()
    digital_value = int(last_return_string)
    print(digital_value)
    if test_digital_value and (digital_value == 1):
        continue
    if (not test_digital_value) and (digital_value == 0):
        continue
    print(f"CH552 serial digital value {digital_value} not match output value {test_digital_value}")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)