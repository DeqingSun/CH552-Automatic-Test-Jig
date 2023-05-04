import time

from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

start_time = time.monotonic()
lines_to_read = 0
while ( (time.monotonic() - start_time) < 10 ):
    ch552_print_data = ch552_serial_code.check_input()
    if len(ch552_print_data) > 0:
        for line in ch552_print_data:
            if 'DataFlash Dump:' in line:
                lines_to_read = 8
            else:
                if lines_to_read > 0:
                    lines_to_read -= 1
                    print(line)
                    if lines_to_read == 0:
                        print("DataFlash Dump complete")
                        #exit(0)
            #print(line)
        #print(ch552_print_data)



ch552_serial_code.disconnect()
exit(0)