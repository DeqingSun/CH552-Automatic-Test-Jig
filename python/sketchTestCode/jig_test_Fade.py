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
#peak detection
delta=1000
max_value=0
min_value=9999
looking_for_peak=looking_for_peak=True
prev_valley_time = 0
prev_peak_time = 0

start_time = time.monotonic()
while ( (time.monotonic() - start_time < 10) and (not fade_verified) ):
    analog_value = ch559_jig.check_analog_pin_subscription(12, wait_for_input_time=1)
    if (analog_value == None):
        print("CH559 jig check_digital_pin_subscription failed")
        exit(1)
    max_value=max(analog_value,max_value)
    min_value=min(analog_value,min_value)
    if (looking_for_peak) :
        if (analog_value<(max_value-delta)) :
            print(f"peak @ {(time.monotonic()-start_time):.2f}")
            if (prev_peak_time != 0):
                peak_interval = time.monotonic() - prev_peak_time
                if (abs(peak_interval-3.0)<0.5) :
                    fade_verified = True
                print(f"peak interval @ {peak_interval:.2f}")
            prev_peak_time = time.monotonic()
            min_value=max_value
            looking_for_peak=False
    else :
        if (analog_value>(min_value+delta)) :
            print(f"valley @ {(time.monotonic()-start_time):.2f}")
            if (prev_valley_time != 0):
                valley_interval = time.monotonic() - prev_valley_time
                if (abs(valley_interval-3.0)<0.5) :
                    fade_verified = True
                print(f"valley interval @ {valley_interval:.2f}")
            prev_valley_time = time.monotonic()
            max_value=min_value
            looking_for_peak=True
    #print(analog_value)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
if not fade_verified:
    print("CH559 jig fade not verified")
    exit(1)
exit(0)