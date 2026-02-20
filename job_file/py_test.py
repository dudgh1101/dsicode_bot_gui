import runpy

filepath = "/Users/user/Desktop/python/example.py"

try:
    runpy.run_path(filepath)
except Exception:
    print("File path is not defined.")

