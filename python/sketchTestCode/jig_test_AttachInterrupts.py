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
return_list = ch552_serial_code.check_input()

ch559_jig.digital_write(25, True, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P32_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
#clear buffer
return_list = ch552_serial_code.check_input()
ch559_jig.digital_write(25, False, wait_for_input_time=1)
time.sleep(0.05)
return_list = ch552_serial_code.check_input()
if ((len(return_list) == 0) or (('Int0 triggered' in return_list[-1]) == False)):
    print("CH552 serial no trigger input")
    exit(1)
ch559_jig.digital_write(25, True, wait_for_input_time=1)
time.sleep(0.05)
return_list = ch552_serial_code.check_input()
if ((len(return_list) > 0)):
    print("CH552 serial printed extra data")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)

ch559_jig.digital_write(25, True, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)
#clear buffer
return_list = ch552_serial_code.check_input()
ch559_jig.digital_write(25, False, wait_for_input_time=1)
time.sleep(0.05)
return_list = ch552_serial_code.check_input()
if ((len(return_list) == 0) or (('Int1 triggered' in return_list[-1]) == False)):
    print("CH552 serial no trigger1 input")
    exit(1)
ch559_jig.digital_write(25, True, wait_for_input_time=1)
time.sleep(0.05)
return_list = ch552_serial_code.check_input()
if ((len(return_list) > 0)):
    print("CH552 serial printed extra data")
    exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)