#mimic the github runner environment
# export GITHUB_WORKSPACE=/home/pi/actions-runner/_work/ch55xduino/ch55xduino
# python selfhost_runner_test.py $GITHUB_WORKSPACE/ch55xduino/ch55x/libraries/Generic_Examples/examples/compiled_hex $GITHUB_WORKSPACE/CH552-Automatic-Test-Jig/python/sketchTestCode $GITHUB_WORKSPACE/ch55xduino/tools/linux_arm/vnproch55x

#this python script takes 3 arguments, the path to the compiled firmwares, the path to test scriptes and the path to the upload tool

import os, sys, time, subprocess
import usb #sudo apt install python3-usb


if(len(sys.argv) < 4):
    print("Usage: python3 selfhost_runner_test.py <path to compiled firmwares> <path to test scripts> <path to upload tool>")
    sys.exit(1)

firmware_path = sys.argv[1]
test_script_directory = sys.argv[2]
upload_tool_path = sys.argv[3]

sys.path.append(test_script_directory)

print("Firmware path: " + firmware_path)
print("Test script path: " + test_script_directory)
print("Upload tool path: " + upload_tool_path)

# check if /etc/udev/rules.d/90-ch551-bl.rules exists
if not os.path.isfile("/etc/udev/rules.d/90-ch551-bl.rules"):
    print("File /etc/udev/rules.d/90-ch551-bl.rules not found. Please create this file with the following content:")
    print('SUBSYSTEM=="usb", ATTRS{idVendor}=="4348", ATTRS{idProduct}=="55e0", MODE="0666"')
    exit(1)

#find all the compiled firmwares in the path (hex)
compiled_firmwares = []
for root, dirs, files in os.walk(firmware_path):
    for file in files:
        if file.endswith(".hex"):
            compiled_firmwares.append(os.path.join(root, file))

if len(compiled_firmwares) == 0:
    print("No compiled firmwares found.")
    exit(1)

compiled_firmwares.sort()

success_count = 0
failure_count = 0

for firmware in compiled_firmwares:
    hex_sketch_name = os.path.basename(firmware).split(".")[0]
    test_script_path = os.path.join(test_script_directory, "jig_test_"+hex_sketch_name+".py")
    if not os.path.isfile(test_script_path):
        print(f"Test script not found at {test_script_path} for {hex_sketch_name}")
        failure_count += 1
        continue
    print(f"Now testing {hex_sketch_name}")
    start_time = time.monotonic()
    #use ch559_jig_code to reboot the CH552 into bootloader mode
    # sketchTestCode is a package in the "test_script_directory" directory
    from ch559_jig_code import CH559_jig
    ch559_jig = CH559_jig()
    ch559_jig.connect()
    if (not ch559_jig.enter_bootloader_mode()):
        print("CH559 jig enter_bootloader_mode failed")
        exit(1)
    ch559_jig.disconnect()
    del ch559_jig
    upload_success = False
    time.sleep(0.5)
    for upload_attempt in range(3):
        #use vnproch55x to upload the hex file
        upload_process = subprocess.Popen([upload_tool_path,"-r","1","-t","CH552",firmware], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = upload_process.communicate() 
        return_code = upload_process.wait()
        if return_code == 0:
            print(f"Upload of {hex_sketch_name} completed after {time.monotonic()-start_time:.2f} seconds")
            upload_success = True
            break
        else:
            print(f"Error uploading {hex_sketch_name}")
            print(out.decode('utf-8'))
            print(err.decode('utf-8'))
            print(f"Try again {upload_attempt+1}/3")
            time.sleep(0.5)

    if not upload_success:
        print(f"Upload of {hex_sketch_name} failed after 3 tries.")
        exit(1)

    test_process = subprocess.Popen(["python",test_script_path], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = test_process.communicate() 
    return_code = test_process.wait()
    if return_code == 0:
        print(f"Test of {hex_sketch_name} completed after {time.monotonic()-start_time:.2f} seconds")
        success_count += 1
    else:
        print(f"Error testing {hex_sketch_name}")
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))
        failure_count += 1
    
print(f"Test completed. Success: {success_count}, Failure: {failure_count}")
if failure_count > 0:
    exit(1)
