from tuning import Tuning
import usb.core
import usb.util
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)
    #print Mic_tuning.direction
    while True:
        if 45 <= Mic_tuning.direction <= 135:
            try:
                print Mic_tuning.direction
                time.sleep(1)
            except KeyboardInterrupt:
                break
        else:
            try: 
                print "OFF"
                time.sleep(1)
            except KeyboardInterrupt:
                break
        