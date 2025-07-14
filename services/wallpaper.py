import ctypes

from os import path, getcwd, makedirs
from shutil import copyfile


def get_wallpaper_path():
    SPI_GETDESKWALLPAPER = 0x0073
    buffer = ctypes.create_unicode_buffer(260)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 260, buffer, 0)
    return buffer.value

def copy_wallpaper(copyTo=None, fileName='wallpaper.jpg'):
    if copyTo is None:
        copyTo = path.join(getcwd(), 'static')
    
    makedirs(copyTo, exist_ok=True)
    dest_path = path.join(copyTo, fileName)
    
    src_path = get_wallpaper_path()
    
    copyfile(src_path, dest_path)
    return dest_path