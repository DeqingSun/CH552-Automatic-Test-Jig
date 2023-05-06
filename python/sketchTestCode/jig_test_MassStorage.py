#haven't found a good way to do this with the current hardware
#just check ID
import time
import os
from ch559_jig_code import CH559_jig

disk_path = ""

from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    start_time = time.monotonic()
    while ((time.monotonic() - start_time < 5) and (disk_path == "")):
        with open("/proc/partitions", "r") as f_partition:
            #get all usb devices
            devices = []
            for line in f_partition.readlines()[2:]: # skip header lines
                words = [ word.strip() for word in line.split() ]
                minor_number = int(words[1])
                device_name = words[3]
                
                if (minor_number % 16) == 0:
                    path = "/sys/class/block/" + device_name
                    
                    if os.path.islink(path):
                        if os.path.realpath(path).find("/usb") > 0:
                            devices.append("/dev/" + device_name)
            for device in devices:
                "/sys/block/%s" % os.path.basename(device)
                path = "/sys/block/%s" % os.path.basename(device) + "/device/model"
                if os.path.exists(path):
                    with open(path, "r") as f:
                        if f.read().strip() == "CH55xduino MSD":
                            print(f"{device} found and ready to mount")
                            if os.path.isdir("/mnt"):
                                os.system("sudo mkdir /mnt/CH55X_MSD")
                                os.system("sudo mount %s /mnt/CH55X_MSD" % device)
                                disk_path = "/mnt/CH55X_MSD"
                                break
                            break
    if disk_path == "":
        print("Cannot find CH55X MSD drive!")
        exit(1)
elif platform == "darwin":
    # OS X
    pass
elif platform == "win32":
    # Windows...
    # find drive with name "CH55X MSD"
    start_time = time.monotonic()
    while ((time.monotonic() - start_time < 5) and (disk_path == "")):
        time.sleep(0.1)
        drive_name = "CH55X MSD"
        for drive in os.popen("wmic logicaldisk get caption,description,providername,volumename"):
            drive = drive.strip()
            if drive.find(drive_name) != -1:
                #print(drive)
                drive_parts = drive.split(" ")
                for part in drive_parts:
                    #print(part)
                    if part.find(":") != -1:
                        disk_path = part
                        break
                break
    if disk_path == "":
        print("Cannot find CH55X MSD drive!")
        exit(1)
    print(f"Using disk path {disk_path} on windows")

readme_path = os.path.join(disk_path, "README.txt")
if not os.path.isfile(readme_path):
    print("Cannot find README.txt!")
    exit(1)
with open(readme_path, 'r') as readme_file:
    readme = readme_file.read()
    if (readme.find("This is a mass storage device example on the Ch55xduino.") == -1):
        print("README.txt does not contain right info")
        exit(1)

long_file_path = os.path.join(disk_path, "LONGFILE.txt")
if not os.path.isfile(long_file_path):
    print("Cannot find long_file.txt!")
    exit(1)
with open(long_file_path, 'r') as long_file:
    long_file_text = long_file.read()
    if (long_file_text.count("*") != 60):
        print("long_file.txt does not contain right info")
        exit(1)


ch559_jig = CH559_jig()

ch559_jig.connect()
if (not ch559_jig.initailize(wait_for_input_time=1)):
    print("CH559 jig initailize failed")
    exit(1)

ch559_jig.connect_pins(ch559_jig.PIN_CH552_P33_X,ch559_jig.PIN_CH559_P25, wait_for_input_time=1)

led_control_file_path = os.path.join(disk_path, "LED_CTRL.txt")
if not os.path.isfile(led_control_file_path):
    print("Cannot find LED_CTRL.txt!")
    exit(1)

try:
    with open(led_control_file_path, 'w') as led_control_file:
        led_control_file.write("1")

    time.sleep(0.1)
    if (ch559_jig.digital_read(25) != True):
        print("LED_CTRL.txt write 1 failed")
        exit(1)

    with open(led_control_file_path, 'w') as led_control_file:
        led_control_file.write("0")

    time.sleep(0.1)
    if (ch559_jig.digital_read(25) != False):
        print("LED_CTRL.txt write 0 failed")
        exit(1)
except PermissionError:
    pass

ch559_jig.initailize(wait_for_input_time=1)
ch559_jig.disconnect()
exit(0)
