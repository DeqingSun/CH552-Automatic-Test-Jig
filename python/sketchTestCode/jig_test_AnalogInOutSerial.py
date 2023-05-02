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
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P34_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_EXT_LED_10_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)

input_values = [0,1,0,1]

for input_value in input_values:
    ch559_jig.digital_write(25, (input_value>0), wait_for_input_time=1)
    time.sleep(0.1)
    return_list = ch552_serial_code.check_input()
    if (len(return_list) == 0):
        print("CH552 serial no input")
        exit(1)
    splited_string = return_list[-1].split()
    sensor_value = int(splited_string[2])
    output_value = int(splited_string[5])
    ideal_output_value = int(input_value*255*3.3/5)
    if (sensor_value != output_value):
        print("CH552 serial not same sensor_value output_value")
        print(sensor_value,output_value)
        exit(1)
    if (abs(sensor_value - ideal_output_value) > 5):
        print("CH552 serial sensor_value not right")
        print(sensor_value,output_value,ideal_output_value)
        exit(1)

    analog_value = ch559_jig.analog_read(12, wait_for_input_time=1)

    ideal_analog_value = int(sensor_value/255*5/3.3*2048)
    ideal_analog_value = min(ideal_analog_value,2047)
    if (abs(analog_value - ideal_analog_value) > 500):
        print(f"CH559 analog_value not right analog_value {analog_value},ideal_analog_value {ideal_analog_value}")
        exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)
