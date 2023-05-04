import time

from ch559_jig_code import CH559_jig
from ch552_serial_code import CH552_serial_code

ch552_serial_code = CH552_serial_code()
ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P31_X,ch559_jig.PIN_CH559_P02, wait_for_input_time=1)
ch559_jig.connect_pins(ch559_jig.PIN_CH552_P30_X,ch559_jig.PIN_CH559_P03, wait_for_input_time=1)

test_uart_rates = [9600,115200]

for test_uart_rate in test_uart_rates:
    print(f"test_uart_rate={test_uart_rate}")
    return_code = ch552_serial_code.connect(test_uart_rate)
    if (return_code != True):
        print("CH552 serial connect failed")
        exit(1)
    ch559_jig.init_uart0(test_uart_rate)
    ch559_jig.uart0_send_string("From CH559!\n")
    time.sleep(0.1)
    ch552_response = ch552_serial_code.check_input()
    if not ("From CH559!" in ch552_response):
        print("From CH559! not found in response")
        print(ch552_response)
        exit(1)
    ch552_serial_code.write_string_wait_for_response("From CH552\n","",0)
    time.sleep(0.1)
    ch559_jig.check_input()
    uart0_string = ch559_jig.uart0_get_buffered_string()
    if not ("From CH552" in uart0_string):
        print("From CH552 not found in response")
        print(uart0_string)
        exit(1)
    ch552_serial_code.disconnect()

ch559_jig.init_uart0(0)
ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)
