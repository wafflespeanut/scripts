import ctypes, socket
from Tkinter import Tk              # ctypes required a slight complication to return cursor position
from math import sin, cos, pi
from time import time, sleep
from urllib2 import urlopen, URLError, HTTPError
event = ctypes.windll.user32
socket.setdefaulttimeout(20)

# Some code to keep a VPN client alive (which usually disconnects in exactly 30 minutes)
# If the application has admin privileges, then Python needs admin privileges to interact with that application

url = 'http://www.youtube.com'

def ping():
    print '\nPinging server...', [url]
    try:
        response = urlopen(url)
    except HTTPError, e:
        print "The server couldn't fulfill the request! Reason:", str(e.code)
        return False
    except URLError, e:
        print 'Failed to reach a server. Reason:', str(e.reason)
        return False
    else:
        html = response.read()
        print 'Got response! '
        return True

def position():
    while True:
        print "\nPlace the cursor at the target - I'll capture it in 5 seconds!"
        root = Tk()
        sleep(5)
        pos = root.winfo_pointerxy()
        print 'Caught the position! ', pos
        root.destroy()
        if not raw_input('Retry (y/n)?\n\n') == 'y':
            return pos
            break

def click(position):
    event.SetCursorPos(position[0], position[1])
    event.mouse_event(2, 0, 0, 0, 0)
    event.mouse_event(4, 0, 0, 0, 0)

def cursor(seconds):                        # To render the cursor inoperative for a few seconds (deprecated)
    i = 0
    later = time() + t
    res = (event.GetSystemMetrics(0), event.GetSystemMetrics(1))
    while time() <= later:
        try:
            x = res[0] / 2 + int(sin(i) * res[0] / 4)
            y = res[1] / 2 + int(cos(i) * res[0] / 4)
            event.SetCursorPos(x, y)
            sleep(.01)
            i += 1
        except KeyboardInterrupt:
            break

def action(p = None):                       # This is what you should run!
    if p == None:
        p = position()
    while True:
        sleep(10)
        if not ping():
            print 'Unable to connect! Clicking...'
            click(p)
            sleep(10)
