import time
import serial
import serial.tools.list_ports

class CH552_serial_code:
    def __init__(self):
        self.serial_port = None
        self.serial_buffer = ""
        

    def connect(self, retry_time=2):
        ch552_port = None
        start_time = time.monotonic()
        while ( (time.monotonic() - start_time < retry_time) and (ch552_port == None) ):
            for port in serial.tools.list_ports.comports():
                if ( ((port.serial_number == "CH55x") and (port.product == "CH55xduino")) or (port.serial_number == "CH55X")):
                    ch552_port = port
                    break

        if (ch552_port == None):
            print("CH55xduino not found")
            return False
        
        #wait for the port to be ready, or there may be SerialException in opening
        time.sleep(0.1)

        try:
            self.serial_port = serial.Serial(ch552_port.device, 115200, timeout=0)
        except Exception as e:
            print("CH55xduino open failed on "+ch552_port.device+" with error: "+type(e).__name__)
            return False
        if (self.serial_port == None):
            print("CH55xduino open failed on "+ch552_port.device)
            return False
        return True
        
    def disconnect(self):
        if (self.serial_port == None):
            return
        self.serial_port.close()
        self.serial_port = None

    def check_input(self):
        return_list = []
        if (self.serial_port == None):
            return return_list
        if (self.serial_port.in_waiting == 0):
            return return_list
        input_bytes = self.serial_port.read(self.serial_port.in_waiting)
        input_string = input_bytes.decode('ascii', errors='ignore')
        while ( (pos_newline := input_string.find('\n')) >=0 ):
            part_before_newline = input_string[0:pos_newline]
            part_after_newline = input_string[pos_newline+1:]
            self.serial_buffer = self.serial_buffer+part_before_newline
            if (len(self.serial_buffer)>0):
                #print(self.serial_buffer)
                return_list.append(self.serial_buffer.strip())
            self.serial_buffer = ""
            input_string = part_after_newline
        return return_list
    
    def write_string_wait_for_response(self, string, string_to_wait,wait_for_input_time):
        if (self.serial_port == None):
            return ""
        if (len(string)>0):
            self.serial_port.write(string.encode('ascii'))
        if (wait_for_input_time == 0):
            #assume the command got processed successfully
            return ""
        else:
            #wait for the input
            if (len(string)>0):
                self.serial_port.flush()
            start_time = time.monotonic()
            while (time.monotonic() - start_time < wait_for_input_time):
                time.sleep(0.001)
                response = self.check_input()
                if (len(response) > 0):
                    for line in response:
                        if string_to_wait in line:
                            return line
            return ""
    
    def write_raw_value(self, raw_value):
        if (self.serial_port == None):
            return ""
        self.serial_port.write(raw_value.to_bytes(1, byteorder='little'))

    def write_bytes(self, bytes_value):
        if (self.serial_port == None):
            return ""
        self.serial_port.write(bytes_value)

    def get_raw_respnse_as_bytes(self, wait_for_input_time=1):
        if (self.serial_port == None):
            return bytes(0)
        start_time = time.monotonic()
        while ( (time.monotonic() - start_time < wait_for_input_time)):
            time.sleep(0.001)
            if (self.serial_port.in_waiting > 0):
                input_bytes = self.serial_port.read(self.serial_port.in_waiting)
                return input_bytes
        return bytes(0)
    