import subprocess
from comtypes import CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

audio_level_multiplier = 655

CoInitialize()
_devices = AudioUtilities.GetSpeakers()
_interface = _devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
_volume_interface = cast(_interface, POINTER(IAudioEndpointVolume))

def get_volume():
    return int(_volume_interface.GetMasterVolumeLevelScalar() * 100)

def change_volume(delta):
    subprocess.call(f"nircmd changesysvolume {delta}", shell=True)

def set_volume(value):
    subprocess.call(f"nircmd setsysvolume {value*audio_level_multiplier}", shell=True)

def toggle_mute():
    subprocess.call("nircmd.exe mutesysvolume 2", shell=True)