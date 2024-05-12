import math
import string
import threading
from threading import Thread
from pynput import mouse
import pyautogui
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import time
import pygetwindow
import psutil
import win32gui
import os
import win32process
import tkinter as tk
from tkinter import ttk


def quits():
    global roblox_hwnd
    global shouldUpdate
    global icon
    global mouse_listener
    mouse_listener.stop()
    shouldUpdate = False
    time.sleep(1)
    win32gui.SetWindowText(roblox_hwnd, "Roblox")
    time.sleep(0.3)
    icon.stop()
    time.sleep(0.99)
    quit()


def settings():
    global warntime
    global sounds_enabled
    bg = "light green"
    root = tk.Tk()
    root.title("◄Settings►")
    root.geometry("170x200+150+150")
    root.attributes("-toolwindow", True)
    root.attributes("-topmost", True)
    root.config(background=bg)
    cont = tk.Frame(root, border=1, borderwidth=2, background=bg)
    cont.pack(anchor="w")
    labeltext = "Warn after x Minutes of AFK"
    label1 = tk.Label(cont, text=labeltext, background=bg, font=("Helvetica", "8", "bold"))
    label1.pack(anchor="w")

    def command(com):
        labeltext = "Warn after " + com + " minutes of AFK"
        if slider1.get() == 0:
            labeltext = "[Disabled]"
            label1.config(foreground="red")
            label1.config(text=labeltext)
        if slider1.get() == 1:
            labeltext = "Warn after a minute of AFK\nRecommended: 15 Minutes"
            label1.config(foreground="red")
            label1.config(text=labeltext)
        if slider1.get() >= 2 and slider1.get() <= 5:
            labeltext = labeltext + "\nRecommended: 15 Minutes"
            label1.config(foreground="red")
            label1.config(text=labeltext)
        if slider1.get() >= 6:
            label1.config(foreground="black")
            label1.config(text=labeltext)

    def command1():
        if normalnumber.get() == 1:
            label2.config(text="[Sounds] [ON]")
        else:
            label2.config(text="[Sounds] [OFF]")

    def command2():
        global warntime
        global sounds_enabled
        wrn = int(slider1.get())
        enbld = int(normalnumber.get())
        if enbld == 0:
            enbld = False
        else:
            enbld = True
        with open("Settings.ini", "w") as f:
            f.write("# Settings file, you can manually change settings here, applied on launch\n")
            f.write("# By deleting this file you will return to default settings\n")
            f.write("Warntime = " + str(wrn) + "\n")
            f.write("Volume = " + str(volume) + "\n")
            f.write("Sounds = " + str(enbld) + "\n")
            warntime = int(wrn)
            sounds_enabled = enbld
            f.close()
        time.sleep(0.2)
        root.destroy()
    val = 0
    if sounds_enabled:
        val = 1
    normalnumber = tk.IntVar(value=int(val), name="value")
    slider1 = tk.Scale(cont, orient="horizontal", background=bg, from_=0, to=20, command=command)
    slider1.config(width=10, length=200, showvalue=False)
    slider1.set(int(warntime))
    slider1.pack(anchor="w")
    label2 = tk.Label(cont, text="[Sounds] [ON]", background=bg)
    label2.pack(anchor="w")
    soundbox1 = tk.Checkbutton(cont, background=bg, command=command1, onvalue=1, offvalue=0, variable=normalnumber)
    soundbox1.pack(anchor="w")
    if sounds_enabled:
        soundbox1.select()
    else:
        soundbox1.deselect()
        label2.config(text="[Sounds] [OFF]")
    closebtn = tk.Button(root, command=command2, text="Save & Exit Settings", background=bg)
    closebtn.pack(side="bottom", pady=5)
    root.mainloop()

def betterSettings():
    thread = threading.Thread(target=settings)
    thread.start()


altx = "AltX"
quitText = "Quit"
start_time = math.floor(time.time())
image = Image.open("icon.jpg")
menu = Menu(MenuItem(quitText, quits), MenuItem("Settings", betterSettings))
icon = Icon(altx, image, altx, menu)
roblox_hwnd = None
roblox_pid = None
shouldUpdate = True
rblxFound = False
roblox_name = "Roblox Logout: [09:39]"
warntime = 15
volume = 0.5
sounds_enabled = False

def target():
    icon.run()


def create_settings_file():
    global warntime
    global volume
    global sounds_enabled
    if not os.path.exists("Settings.ini"):
        with open("Settings.ini", "w") as f:
            f.write("# Settings file, you can manually change settings here, applied on launch\n")
            f.write("# By deleting this file you will return to default settings\n")
            f.write("Warntime = " + str(warntime) + "\n")
            f.write("Volume = " + str(volume) + "\n")
            f.write("Sounds = " + str(sounds_enabled) + "\n")
            f.close()
    if os.path.exists("Settings.ini"):
        with open("Settings.ini", "r") as f:
            filestring = f.readlines()
            index = 0
            while index < len(filestring):
                if str(filestring[index])[0] != "#" and len(str(filestring[index])) >= 3:
                    file = filestring[index].rstrip("\n")
                    if file.find("Warntime = ") == 0:
                        file = file.strip("Warntime = ")
                        warntime = int(file)
                    if file.find("Volume = ") == 0:
                        file = file.strip("Volume = ")
                        volume = float(file)
                    if file.find("Sounds = ") == 0:
                        file = file.strip("Sounds = ")
                        if file == "False":
                            sounds_enabled = False
                        else:
                            sounds_enabled = True
                index += 1
    print("Warntime:", warntime, "Minutes")
    print("Volume:", volume)
    print("Sounds:", sounds_enabled)

def findRoblox():
    global roblox_pid
    global roblox_hwnd
    global rblxFound
    for process in psutil.process_iter(['pid', 'name']):
        if process.name() == "RobloxPlayerBeta.exe":
            roblox_pid = process.pid
            windows = pygetwindow.getAllWindows()
            xid = 0
            for x in windows:
                if x.title == "Roblox":
                    lister = str(windows).split()
                    lister = lister[xid].strip("Win32Window")
                    lister = lister.strip("(hWnd=")
                    lister = lister.strip("),")
                    roblox_hwnd = lister
                if str(x.title).find("Roblox Logout: ") == 0:
                    lister = str(windows).split()
                    lister = lister[xid].strip("Win32Window")
                    lister = lister.strip("(hWnd=")
                    lister = lister.strip("),")
                    roblox_hwnd = lister
                xid = xid + 1
            print("PID:", roblox_pid)
            print("hWnd:", roblox_hwnd)
            print("Process:", process.name())
            rblxFound = True
    time.sleep(1)
    if not rblxFound:
        thread = threading.Thread(target=findRoblox)
        thread.start()


def writeRoblox():
    global shouldUpdate
    global roblox_pid
    global roblox_hwnd
    global roblox_name
    global start_time
    global warntime
    maxtime = int(60 * 20)
    while shouldUpdate:
        currentTime = math.floor(time.time())
        timeleft = (maxtime - math.floor(currentTime - start_time))
        minute = math.floor(timeleft / 60)
        second = math.floor(timeleft - (minute * 60))
        minute = str(minute)
        second = str(second)
        if len(minute) == 1:
            minute = "0" + minute
        if len(second) == 1:
            second = "0" + second
        roblox_name = "Roblox Logout: [" + str(minute) + ":" + str(second) + "]"
        win32gui.SetWindowText(roblox_hwnd, roblox_name)
        time.sleep(1)


def detector(mouse_position_x, mouse_position_y, button, is_pressed):
    global shouldUpdate
    t_time = int(math.floor(time.time()))
    if not shouldUpdate:
        return

    def unit():
        global start_time
        global roblox_hwnd
        if not str(roblox_hwnd) == str(win32gui.GetForegroundWindow()):
            return
        if not shouldUpdate:
            return
        time.sleep(0.225)
        if not str(roblox_hwnd) == str(win32gui.GetForegroundWindow()):
            return
        if not shouldUpdate:
            return
        time.sleep(0.225)
        if not shouldUpdate:
            return
        if not str(roblox_hwnd) == str(win32gui.GetForegroundWindow()):
            return
        if str(button) == "Button.left":
            if is_pressed:
                if str(roblox_hwnd) == str(win32gui.GetForegroundWindow()):
                    start_time = t_time
        if str(button) == "Button.right":
            if is_pressed:
                if str(roblox_hwnd) == str(win32gui.GetForegroundWindow()):
                    start_time = t_time

    thread = threading.Thread(target=unit)
    thread.start()


mouse_listener = mouse.Listener(on_click=detector)


def starter():
    create_settings_file()
    thread = Thread(target=target)
    thread.start()
    thread2 = threading.Thread(target=findRoblox)
    thread2.start()
    global rblxFound
    global mouse_listener
    while not rblxFound:
        time.sleep(0.2)
    mouse_listener.start()
    writeRoblox()


starter()
