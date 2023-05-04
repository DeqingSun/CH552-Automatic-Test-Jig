import time

from ch559_jig_code import CH559_jig
from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()
ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.reboot_target()

time.sleep(0.5)

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

all_text = ""

found_text_ASCII_Table = False
found_text_dec_126 = False

start_time = time.monotonic()
while (time.monotonic() - start_time < 5):
    return_list = ch552_serial_code.check_input()
    if (len(return_list) > 0):
        #join all the text in list return_list together
        all_text = all_text + '\n'.join(return_list)
        if ("ASCII Table" in all_text):
            found_text_ASCII_Table = True
        if ("dec: 126" in all_text):
            found_text_dec_126 = True
        if (found_text_ASCII_Table and found_text_dec_126):
            exit(0)
print(all_text)
exit(1)

    
