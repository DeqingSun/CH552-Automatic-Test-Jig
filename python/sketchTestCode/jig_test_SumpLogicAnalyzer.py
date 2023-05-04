import time

from ch559_jig_code import CH559_jig
from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()
ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.analog_write(25, 128, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P14_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)

return_code = ch552_serial_code.connect()
if (return_code != True):
    print("CH552 serial connect failed")
    exit(1)

ch552_serial_code.write_raw_value(0x02)
byte_response = ch552_serial_code.get_raw_respnse_as_bytes()
if (byte_response != b'1ALS'):
    print("SUMP_QUERY failed")
    print(byte_response)
    exit(1)

ch552_serial_code.write_raw_value(0x04)
byte_response = ch552_serial_code.get_raw_respnse_as_bytes()
if ("AGLA CH55x").encode() not in byte_response:
    print("SUMP_GET_METADATA failed")
    print(byte_response)
    exit(1)

sample_rates_MHZ = [5,1]
for sample_rate_MHZ in sample_rates_MHZ:
    print(f"sample_rate_MHZ={sample_rate_MHZ}")
    divider_array = [0x80,(int)(100/sample_rate_MHZ)-1,0,0,0]
    ch552_serial_code.write_bytes(bytes(divider_array))
    time.sleep(0.05)
    ch552_serial_code.write_bytes(b'\x01')
    time.sleep(0.1)
    byte_response = ch552_serial_code.get_raw_respnse_as_bytes()
    if (len(byte_response) != 1480):
        print(f"byte_response length not correct as {len(byte_response)}")
        print(byte_response)
        exit(1)

    index_count = 0
    prev_level = False
    prev_level_start_index = 0
    level_durations = []
    for singleByte in byte_response:
        current_level = ((singleByte & 0x1) != 0)
        if (current_level != prev_level):
            level_duration = index_count - prev_level_start_index
            if (level_duration > 0):
                level_durations.append(level_duration)
            prev_level = current_level
            prev_level_start_index = index_count
        index_count = index_count + 1
    level_durations.append(index_count - prev_level_start_index)

    ideal_level_duration=sample_rate_MHZ*1000*1000/(4*1000)/2 # 4MHz clock, 50% duty cycle at 5M sample rate

    #iterate level_durations except the first one and the last one
    for level_duration in level_durations[1:-1]:
        if (level_duration < ideal_level_duration*0.9 or level_duration > ideal_level_duration*1.1):
            print(f"level_duration={level_duration} is not ideal as {ideal_level_duration}")
            print(level_durations)
            exit(1)

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
ch552_serial_code.disconnect()
exit(0)
