import time

from ch559_jig_code import CH559_jig

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P26, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_11_X,ch559_jig.PIN_CH559_P26, wait_for_input_time=1)
pin_value = ch559_jig.digital_pin_subscribe(26, wait_for_input_time=1)

test_digital_values = [False, True, False, True, False, True]
for test_digital_value in test_digital_values:
    ch559_jig.digital_write(25, test_digital_value, wait_for_input_time=1)
    time.sleep(0.1)
    pin_value = ch559_jig.check_digital_pin_subscription(26, wait_for_input_time=1)
    if (pin_value == None):
        print("CH559 jig check_digital_pin_subscription failed")
        exit(1)
    if test_digital_value and (pin_value == False):
        continue
    if (not test_digital_value) and (pin_value == True):
        continue
    print(f"CH552 serial digital value {pin_value} not match output value {test_digital_value}")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)