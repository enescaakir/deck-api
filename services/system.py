import subprocess

def shutdown():
    subprocess.call("nircmd.exe exitwin poweroff")

def standby():
    subprocess.call("nircmd.exe standby")

def lock_screen():
    subprocess.call("rundll32.exe user32.dll,LockWorkStation")
