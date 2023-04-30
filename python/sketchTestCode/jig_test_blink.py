import time
from ch559_jig_code import CH559_jig

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connectPins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
ch559_jig.connectPins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
pin_value = ch559_jig.digitalPinSubscribe(25, wait_for_input_time=1)

#measure toggle time
start_time = time.monotonic()
prev_pin_value = pin_value
pin_toggle_time = time.monotonic()
toggle_duration_history = []
toggle_duration_verified = False
while ( (time.monotonic() - start_time < 10) and (not toggle_duration_verified) ):
    pin_value = ch559_jig.checkDigitalPinSubscription(25, wait_for_input_time=1)
    if (pin_value == None):
        print("CH559 jig checkDigitalPinSubscription failed")
        exit(1)
    if (prev_pin_value != pin_value):
        toggle_duration = time.monotonic() - pin_toggle_time
        toggle_duration_history.append(toggle_duration)
        if (len(toggle_duration_history) > 2):
            toggle_duration_history.pop(0)
        pin_toggle_time = time.monotonic()
        prev_pin_value = pin_value
        if (len(toggle_duration_history)==2):
            #check if the toggle durations are between 0.95 and 1.05 seconds
            if ( (toggle_duration_history[0] > 0.95) and (toggle_duration_history[0] < 1.05) and
                 (toggle_duration_history[1] > 0.95) and (toggle_duration_history[1] < 1.05) ):
                toggle_duration_verified = True
                break
if not toggle_duration_verified:
    print("CH559 jig toggle duration not verified")
    exit(1)
ch559_jig.disconnect()
exit(0)