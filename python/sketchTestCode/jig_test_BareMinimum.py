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

ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)
