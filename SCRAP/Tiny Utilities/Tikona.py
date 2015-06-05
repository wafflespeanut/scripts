execfile("Stable VPN.py")
import os
url = 'http://www.youtube.com'

def check():
    count = 0
    while True:
        sleep(60)
        if ping():
            count = 0
        else:
            count += 1
        if count > 30:
            os.system('shutdown /h')            # Only for now - I'll update it to send POST requests later
