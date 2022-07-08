# Connecting to wifi, sending data thorugh wifi
WIFI_NAME = "Something"
WIFI_PASSWORD = "Something"

def do_connect():
    from network import WLAN
    import time
    import pycom
    import machine
    pycom.wifi_mode_on_boot(WLAN.STA)   # choose station mode on boot
    wlan = WLAN() # get current object, without changing the mode
    # Set STA on soft rest
    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.init(mode=WLAN.STA)        # Put modem on Station mode
    if not wlan.isconnected():          # Check if already connected
        print("Connecting to WiFi...")
        # Connect with your WiFi Credential
        wlan.connect(WIFI_NAME, auth=(WLAN.WPA2, WIFI_PASSWORD))
        # Check if it is connected otherwise wait
        while not wlan.isconnected():
            pass
    print("Connected to Wifi")
    time.sleep_ms(500)
    # Print the IP assigned by router
    print('network config:', wlan.ifconfig(id=0))

do_connect()
