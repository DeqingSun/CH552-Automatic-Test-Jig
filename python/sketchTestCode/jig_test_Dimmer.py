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

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P34_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)

value_to_writes = [0,64,128,192,255]

for value_to_write in value_to_writes:
    ch552_serial_code.write_raw_value(value_to_write)
    time.sleep(0.1)
    analog_value=ch559_jig.analog_read(12, wait_for_input_time=1)
    ideal_value = int(value_to_write*5/3.3/255*2047)
    ideal_value = min(ideal_value,2047)
    if (abs(analog_value-ideal_value)>400):
        print("analog_value-ideal_value>400")
        print(analog_value,ideal_value)
        exit(1)
        
ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)
