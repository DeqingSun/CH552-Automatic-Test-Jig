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

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P11_X,ch559_jig.PIN_CH559_P12_RC, wait_for_input_time=1)

test_pwm_values = [0,64,128,192,255]
for test_pwm_value in test_pwm_values:
    ch552_calculated_read_value = test_pwm_value*3.3/5.0    #CH552 ADC is 8-bit, 5V. CH559 PWM3 is 8-bit, 3.3V
    ch559_jig.analog_write(12, test_pwm_value, wait_for_input_time=1)
    time.sleep(0.1)
    return_list = ch552_serial_code.check_input()
    if (len(return_list) == 0):
        print("CH552 serial no input")
        exit(1)

    average_samples = min(4,len(return_list))
    sum = 0
    for i in range(average_samples):
        return_string = return_list[-1-i].strip()
        sum = sum + int(return_string)
    adc_value = sum/average_samples

    if (abs(adc_value - ch552_calculated_read_value) > 5):
        print(f"CH552 serial ADC value {adc_value} not match calculated value {ch552_calculated_read_value}")
        exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)
