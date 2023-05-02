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
ch559_jig.digital_write(25, True, wait_for_input_time=1)
time.sleep(0.1)
start_pin_value = ch559_jig.check_digital_pin_subscription(26, wait_for_input_time=1)
if (pin_value == None):
    print("CH559 jig check_digital_pin_subscription failed")
    exit(1)
print(f"start_pin_value {start_pin_value}")
ch559_jig.digital_write(25, False, wait_for_input_time=1)
ch559_jig.digital_write(25, True, wait_for_input_time=1)
time.sleep(0.1)
pin_value = ch559_jig.check_digital_pin_subscription(26, wait_for_input_time=1)
print(f"short pulse pin_value {pin_value}")
if (pin_value != start_pin_value):
    print("debounce failed")
    exit(1)
time.sleep(0.1)
ch559_jig.digital_write(25, False, wait_for_input_time=1)
time.sleep(0.1)
ch559_jig.digital_write(25, True, wait_for_input_time=1)
time.sleep(0.1)
pin_value = ch559_jig.check_digital_pin_subscription(26, wait_for_input_time=1)
print(f"long pulse pin_value {pin_value}")
if (pin_value == start_pin_value):
    print("no debounce failed")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)