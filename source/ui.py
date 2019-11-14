import tkinter as tk
from source.porthandler import openports
from source.maps import *
import threading
import sys

def apply(inport, outport, newscale, newkey, inports, outports):
    global midiin, midiout, scale, key
    scale = newscale
    key = newkey
    midiin, midiout = openports(inports.index(bytes(inport[2:-1], "utf-8")), outports.index(bytes(outport[2:-1], "utf-8")))

def harmonize(pitch, scale, key):
    note = pitch % 12
    octave = pitch // 12
    if scale == "minor":
        note = minormap[note]
    if scale == "major":
        pass
    note = note + keymap[key]
    newpitch = note + 12 * octave
    return newpitch

def run():
    global midiin, midiout, key, scale, running
    running = True
    while running:
        try:
            midiag = midiin.get_message()
            if midiag != (None, None):
                print(midiag)
                status, pitch, velocity = midiag[0]
                newpitch = harmonize(pitch, scale, key)
                midiout.send_message([status, newpitch, velocity])
        except NameError:
            #no midi devices selected
            pass 

def on_closing():
    global midiout, midiin, midithread, root, running
    del midiout, midiin
    running = False
    root.destroy()
    sys.exit()

def backgroundthread():
    global midithread
    print("penis")
    midithread = threading.Thread(target=run)
    midithread.start()

def _uisetup(inports: list, outports: list):
    global root

    root = tk.Tk()
    root.title("EPIC AUTOMIDIHARMONIZER")
    root.geometry('350x150')
    root.resizable(False, False)
    # devices
    deviceframe = tk.Frame(root, pady=10)
    deviceframe.pack(side=tk.TOP)
    outportvar, inportvar = tk.StringVar(deviceframe), tk.StringVar(deviceframe)
    outportvar.set(outports[0])
    inportvar.set(inports[0])
    setinports, setoutports = set(inports), set(outports)
    outportmenu = tk.OptionMenu(deviceframe, outportvar, *setoutports)
    outportmenu.pack(side=tk.LEFT)
    inportmenu = tk.OptionMenu(deviceframe, inportvar, *setinports)
    inportmenu.pack(side=tk.LEFT)
    # scales
    scaleframe = tk.Frame(root)
    scaleframe.pack(side=tk.TOP)
    scales = {"major", "minor"}
    keys = sorted({'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B'})
    scalevar, keyvar = tk.StringVar(scaleframe), tk.StringVar(scaleframe)
    scalevar.set("major")
    keyvar.set("C")
    scalemenu = tk.OptionMenu(scaleframe, scalevar, *scales)
    scalemenu.pack(side=tk.LEFT)
    keymenu = tk.OptionMenu(scaleframe, keyvar, *keys)
    keymenu.pack(side=tk.LEFT)
    # apply button
    applyframe = tk.Frame(root, pady=10)
    applyframe.pack(side=tk.BOTTOM)
    applybutton = tk.Button(applyframe, text=" Apply ", command=lambda: apply(inportvar.get(), outportvar.get(), scalevar.get(), keyvar.get(), inports, outports))
    applybutton.pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(200, backgroundthread)

def runui():
    root.mainloop()