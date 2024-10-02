import sys

def is_running_in_virtualenv():
    return sys.prefix != sys.base_prefix

print(sys.prefix)
print(sys.base_prefix)
if is_running_in_virtualenv():
    print("Python is running inside virtualenv.")
else:
    print("Python is not running inside virtualenv.")
