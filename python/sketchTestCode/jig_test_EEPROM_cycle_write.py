import time

from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

start_time = time.monotonic()
data_to_read = 0
eeprom_data_old = [0]
eeprom_data = []

eeprom_check_ok = False

while ( (time.monotonic() - start_time) < 15 and not eeprom_check_ok):
    ch552_print_data = ch552_serial_code.check_input()
    if len(ch552_print_data) > 0:
        for line in ch552_print_data:
            if 'DataFlash Dump:' in line:
                eeprom_data_old = eeprom_data
                eeprom_data = []
                data_to_read = 128
            else:
                if data_to_read > 0:
                    line_to_process = line
                    try:
                        while( len(line_to_process)>=3 and line_to_process[2] == ',' ):
                            eeprom_data.append(int(line_to_process[0:2],16))
                            line_to_process = line_to_process[3:]
                            data_to_read -= 1
                    except:
                        print("Error in parsing line: "+line)
                        data_to_read = 0

                    if len(eeprom_data) == 128:
                        print(f"EEPROM data read on {time.monotonic()-start_time:02f}:")
                        print((eeprom_data))
                        if len(eeprom_data_old) == 128:
                            #check difference between old and new data
                            for i in range(128):
                                if eeprom_data[i] != eeprom_data_old[i]:
                                    print(f"new data {eeprom_data[i]} @ {i}")
                                    if (eeprom_data[i] & 127) == i:
                                        eeprom_check_ok = True
                                    break

ch552_serial_code.disconnect()

if eeprom_check_ok:
    print("EEPROM check OK")
    exit(0)
else:
    print("EEPROM check failed")
exit(1)