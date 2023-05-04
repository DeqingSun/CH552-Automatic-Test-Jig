#haven't found a good way to do this with the current hardware
#just check ID
from sys import platform
if platform == "linux" or platform == "linux2":
    pass    
    #check usb descriptors only with lsusb
    exit(1) 
    # linux
elif platform == "darwin":
    # OS X  //skip test
    exit(0)
elif platform == "win32":
    # Windows...    //skip test
    exit(0)

