import yaml
import os
import subprocess
import time

need_to_build = True

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

if need_to_build:
    #clear folders
    os.system(f"rm -rf folder {os.path.join(arduino_build_directory, '*')}")
    os.system(f"rm -rf folder {os.path.join(arduino_core_build_directory, '*')}")
    os.system(f"rm -rf folder {os.path.join(batch_build_directory, '*')}")
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
        build_cmd = f"{arduino_cli_path} compile --fqbn CH55xDuino:mcs51:ch552 --build-path {arduino_build_directory} --build-cache-path {arduino_core_build_directory} {example_directory}"
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
                os.system(f"cp {hex_path} {batch_build_directory}")
            else:
                print(f"Hex file not found at {hex_path}")
        else:
            #append output to error log file
            err_string = err.decode('utf-8')
            print(f"Error building {example_name}")
            with open(error_log_file, 'a') as error_log:
                error_log.write(f"===\nError building {example_name}\n")
                error_log.write(err_string)
