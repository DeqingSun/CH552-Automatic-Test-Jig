#haven't found a good way to do this with the current hardware
#just check ID
import time
import usb
import os
from usb.backend import libusb1

from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    pass    
elif platform == "darwin":
    # OS X
    pass
elif platform == "win32":
    # Windows...
    #find current path of script
    script_path = os.path.dirname(os.path.realpath(__file__))
    dll_path = os.path.join(script_path, "windowsDLL")
    dll_path = os.path.join(dll_path, "libusb-1.0.dll")
    #print(dll_path)
    backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)
    usb_devices = usb.core.find(backend=backend, find_all=True)

time.sleep(1)

usbtinyISP_device = None

for busses in usb.busses():
    for device in busses.devices:
        if device.idVendor == 0x1781 and device.idProduct == 0x0C9F:
            usbtinyISP_device = device
if usbtinyISP_device == None:
    print("usbtinyISP not found")
    exit(1)

#windows can not get string in descriptor, that's it
exit(0)
