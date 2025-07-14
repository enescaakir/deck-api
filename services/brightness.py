import screen_brightness_control as sbc

#You can customize here if you have multiple screen but different brands or models to sync brightness levels
second_monitor_brightness_additional_value = 30

def get_brightness():
    return sbc.get_brightness()

def set_brightness(value):
    for monitor in sbc.list_monitors():
        if monitor == 'Philips 246V5': #Changes here if you want
            value += second_monitor_brightness_additional_value
        sbc.set_brightness(value, monitor)

#Use this on main to get your monitors list
def get_monitors():
    return sbc.list_monitors()