import yaml
import os
import subprocess
import time
import shutil

need_to_build = False
need_to_test = True

with open("config.yaml", 'r') as stream:
    arduino_config = yaml.safe_load(stream)

arduino_cli_path = arduino_config['arduino_cli_path']
print(f"Using Arduion CLI at {arduino_cli_path}")
if not os.path.isfile(arduino_cli_path):
    print(f"arduino-cli not found at {arduino_cli_path}")
    exit(1)
arduino_build_directory = arduino_config['arduino_build_directory']
print(f"Using Arduino build directory at {arduino_build_directory}")
if not os.path.isdir(arduino_build_directory):
    print(f"arduino build directory not found at {arduino_build_directory}")
    exit(1)
arduino_core_build_directory = arduino_config['arduino_core_build_directory']
print(f"Using Arduino core build directory at {arduino_core_build_directory}")
if not os.path.isdir(arduino_core_build_directory):
    print(f"arduino core build directory not found at {arduino_core_build_directory}")
    exit(1)
batch_build_directory = arduino_config['batch_build_directory']
print(f"Using batch build directory at {batch_build_directory}")
if not os.path.isdir(batch_build_directory):
    print(f"batch build directory not found at {batch_build_directory}")
    exit(1)
example_search_directory = arduino_config['example_search_directory']
print(f"Using example search directory at {example_search_directory}")
if not os.path.isdir(example_search_directory):
    print(f"example search directory not found at {example_search_directory}")
    exit(1)
error_log_file = arduino_config['error_log_file']
print(f"Using error log file at {error_log_file}")
upload_tool_path = arduino_config['upload_tool_path']
print(f"Using upload tool path at {upload_tool_path}")
if not os.path.isfile(upload_tool_path):
    print(f"upload tool not found at {upload_tool_path}")
    exit(1)
test_script_directory = arduino_config['test_script_directory']
print(f"Using test script directory at {test_script_directory}")
if not os.path.isdir(test_script_directory):
    print(f"test script directory not found at {test_script_directory}")
    exit(1)

if need_to_build:
    #clear folders
    folders_to_clear = [arduino_build_directory, arduino_core_build_directory, batch_build_directory]
    for folder in folders_to_clear:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    #iterate every sub folder in the example_search_directory
    example_directories = []
    for subdir, dirs, files in os.walk(example_search_directory):
        dirs.sort()
        for dir in dirs:
            potential_example_directory = os.path.join(subdir, dir)
            example_ino_name = dir + ".ino"
            example_ino_full_path = os.path.join(potential_example_directory, example_ino_name)
            if os.path.isfile(example_ino_full_path):
                example_directories.append(potential_example_directory)
                #print(f"Found example at {potential_example_directory}")

    #print(example_directories)
    for example_directory in example_directories:
        board_options_string = ""
        sketch_file = os.path.join(example_directory, os.path.basename(example_directory)+".ino")
        #check if there is a line in the sketch file that contains "cli board options:"
        if os.path.isfile(sketch_file):
            with open(sketch_file, 'r') as fp:
                lines = fp.readlines()
                for row in lines:
                    if row.find('cli board options:') != -1:
                        board_options_string = '--board-options '+row.replace('cli board options:', '').strip()
                        break

        build_cmd = f"{arduino_cli_path} compile --fqbn CH55xDuino:mcs51:ch552 --build-path {arduino_build_directory} --build-cache-path {arduino_core_build_directory} {example_directory}"
        if board_options_string != "":
            build_cmd = build_cmd + " " + board_options_string
        example_name = os.path.basename(example_directory)
        print(f"Building {example_name}")
        build_start_time = time.monotonic()
        build_process = subprocess.Popen(build_cmd.split(" "), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = build_process.communicate() 
        build_end_time = time.monotonic()
        build_time = build_end_time - build_start_time
        return_code = build_process.wait()
        if return_code == 0:
            print(f"Build of {example_name} completed in {build_time:.2f} seconds")
            hex_path = os.path.join(arduino_build_directory, example_name+".ino.hex")
            if os.path.isfile(hex_path):
                shutil.copy(hex_path, batch_build_directory)
            else:
                print(f"Hex file not found at {hex_path}")
        else:
            #append output to error log file
            err_string = err.decode('utf-8')
            print(f"Error building {example_name}")
            with open(error_log_file, 'a') as error_log:
                error_log.write(f"===\nError building {example_name}\n")
                error_log.write(err_string)

if need_to_test:
    #iterate every file in the batch_build_directory in date order
    hex_files = []
    for subdir, dirs, files in os.walk(batch_build_directory):
        for file in files:
            if file.endswith(".hex"):
                hex_files.append(os.path.join(subdir, file))
    hex_files.sort(key=os.path.getmtime)
    #for debug purposes
    hex_files = hex_files[0:5]
    for hex_file in hex_files:
        #find corresponding test script
        hex_sketch_name = os.path.basename(hex_file).split(".")[0]
        test_script_path = os.path.join(test_script_directory, "jig_test_"+hex_sketch_name+".py")
        if not os.path.isfile(test_script_path):
            print(f"Test script not found at {test_script_path} for {hex_sketch_name}")
            continue
        print(f"Now testing {hex_file}")
        #use ch559_jig_code to reboot the CH552 into bootloader mode
        from sketchTestCode.ch559_jig_code import CH559_jig
        ch559_jig = CH559_jig()
        ch559_jig.connect()
        if (not ch559_jig.enter_bootloader_mode()):
            print("CH559 jig enter_bootloader_mode failed")
            exit(1)
        ch559_jig.disconnect()
        del ch559_jig
        #use vnproch55x to upload the hex file
        upload_process = subprocess.Popen([upload_tool_path,"-r","2",hex_file], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = upload_process.communicate() 
        return_code = upload_process.wait()
        if return_code == 0:
            print(f"Upload of {hex_file} completed")
        else:
            print(f"Error uploading {hex_file}")
            with open(error_log_file, 'a') as error_log:
                error_log.write(f"Error uploading {hex_file}\n")
            exit(1)
        test_process = subprocess.Popen(["python",test_script_path], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = test_process.communicate() 
        return_code = test_process.wait()
        if return_code == 0:
            print(f"Test of {hex_file} completed")
        else:
            print(f"Error testing {hex_file}")
            print(out.decode('utf-8'))
            print(err.decode('utf-8'))
            with open(error_log_file, 'a') as error_log:
                error_log.write(f"Error testing {hex_file}\n")
            exit(1)
        

        
