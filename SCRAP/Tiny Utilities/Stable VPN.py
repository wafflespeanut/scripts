import ctypes
from Tkinter import Tk              # ctypes required a slight complication to return cursor position
from math import sin,cos,pi
from time import sleep
event=ctypes.windll.user32; root=Tk()

res=(event.GetSystemMetrics(0),event.GetSystemMetrics(1))

def position():
    print "Place the cursor at the target - I'll capture in 5 seconds!\n"
    sleep(5); p=root.winfo_pointerxy(); print 'Caught the position!',p
    click(p); print 'Clicking now...'

def click(p):
    event.SetCursorPos(p[0],p[1])
    event.mouse_event(2,0,0,0,0); event.mouse_event(4,0,0,0,0)

def action():
    i=0; p=position()
    while True:
        try:
            x=res[0]/2+int(sin(pi*i/100)*res[0]/3); y=res[1]/2+int(cos(i)*100)
            event.SetCursorPos(x,y); sleep(.01); i+=1
        except KeyboardInterrupt: break

