#run jig_test_Blink.py and get the return code
import subprocess
import os

#find path of self
self_path = os.path.dirname(os.path.realpath(__file__))
blink_script_path = os.path.join(self_path, "jig_test_Blink.py")
blink_test_process = subprocess.Popen(["python",blink_script_path], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = blink_test_process.communicate()
return_code = blink_test_process.wait()
exit(return_code)