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

cmsis_dap_device = None

for busses in usb.busses():
    for device in busses.devices:
        if device.idVendor == 0x1209 and device.idProduct == 0xc55d:
            cmsis_dap_device = device

if cmsis_dap_device == None:
    print("CMSIS-DAP not found")
    exit(1)

#windows can not get string in descriptor, that's it
exit(0)
