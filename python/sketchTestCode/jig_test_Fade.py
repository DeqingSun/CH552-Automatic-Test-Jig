import time
from ch559_jig_code import CH559_jig

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P34_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)

analog_value = ch559_jig.analog_pin_subscribe(12, wait_for_input_time=1)
fade_verified = False
start_time = time.monotonic()
while ( (time.monotonic() - start_time < 10) and (not fade_verified) ):
     analog_value = ch559_jig.check_analog_pin_subscription(12, wait_for_input_time=1)
     if (analog_value == None):
         print("CH559 jig check_digital_pin_subscription failed")
         exit(1)
     print(analog_value)

# ch559_jig.initailize(wait_for_input_time=1)
# ch559_jig.disconnect()
# exit(0)