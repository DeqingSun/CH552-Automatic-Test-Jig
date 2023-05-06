import time

from ch559_jig_code import CH559_jig
from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

response = ch552_serial_code.write_string_wait_for_response("echo Test\n","ECHO:echo Test", wait_for_input_time=1)
if len(response) == 0:
    print("ECHO:echo Test failed")
    exit(1)

ch552_serial_code.disconnect()
exit(0)