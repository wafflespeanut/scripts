import ctypes
from Tkinter import Tk              # ctypes requires a complication to return cursor position
from math import sin,cos,pi
from time import sleep
event=ctypes.windll.user32; root=Tk()

# Though win32api is awesome, I don't wanna bother my fellas by making use of a lot of dependancies

res=(event.GetSystemMetrics(0),event.GetSystemMetrics(1))

def position():
    print "Place the cursor at the target - I'll capture in 5 seconds!\n"
    sleep(5); return root.winfo_pointerxy()

def action():
    i=0
    while True:
        try:
            x=res[0]/2+int(sin(pi*i/100)*500); y=res[1]/2+int(cos(i)*100)
            event.SetCursorPos(x,y); sleep(.01); i+=1
        except KeyboardInterrupt: break

