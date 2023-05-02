import time
from ch559_jig_code import CH559_jig

ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
pin_value = ch559_jig.digital_pin_subscribe(25, wait_for_input_time=1)

test_pwm_values = [128,255]
for test_pwm_value in test_pwm_values:
    ch559_jig.analog_write(12, test_pwm_value, wait_for_input_time=1)
    ch552_calculated_toggle_duration = (test_pwm_value*3.3/5)/1000
    print(f"CH552 calculated toggle duration {ch552_calculated_toggle_duration:.2f}")

    #measure toggle time
    start_time = time.monotonic()
    prev_pin_value = pin_value
    pin_toggle_time = time.monotonic()
    toggle_duration_history = []
    toggle_duration_verified = False
    while ( (time.monotonic() - start_time < 10) and (not toggle_duration_verified) ):
        pin_value = ch559_jig.check_digital_pin_subscription(25, wait_for_input_time=1)
        if (pin_value == None):
            print("CH559 jig check_digital_pin_subscription failed")
            exit(1)
        if (prev_pin_value != pin_value):
            toggle_duration = time.monotonic() - pin_toggle_time
            #print(f"CH552 toggle duration {toggle_duration:.2f}")
            toggle_duration_history.append(toggle_duration)
            if (len(toggle_duration_history) > 2):
                toggle_duration_history.pop(0)
            pin_toggle_time = time.monotonic()
            prev_pin_value = pin_value
            if (len(toggle_duration_history)==2):
                #check if the toggle durations are between 0.95 and 1.05 seconds
                if ( abs(toggle_duration_history[0] - ch552_calculated_toggle_duration) < 0.05 and
                    abs(toggle_duration_history[1] - ch552_calculated_toggle_duration) < 0.05 ):
                    toggle_duration_verified = True
                    break
    if not toggle_duration_verified:
        print("CH559 jig toggle duration not verified")
        exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)