import tkinter as tk
from ttkthemes import ThemedTk
from source.porthandler import openports
from source.maps import *
import threading
import sys, os, base64
from icon import img


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
    try:
        del midiout, midiin
    except NameError:
        pass
    running = False
    root.destroy()
    sys.exit()

def backgroundthread():
    global midithread
    midithread = threading.Thread(target=run)
    midithread.start()

def _uisetup(inports: list, outports: list):
    global root

    iconfile = "favicon.ico" 
    if not hasattr(sys, "frozen"):
        iconfile = os.path.join(os.path.dirname(__file__), iconfile) 
    else:  
        iconfile = os.path.join(sys.prefix, iconfile)

    root = ThemedTk(theme="arc")
    root.title("AMH")
    root.configure(padx=10, pady=8)
    root.resizable(False, False)
    # input
    inportvar = tk.StringVar(root)
    inportlabel = tk.ttk.Label(root, text="IN:")
    inportlabel.grid(row=0, column=0)
    inportmenu = tk.ttk.OptionMenu(root, inportvar, inports[0], *inports)
    inportmenu.grid(row=0, column=1, sticky=tk.W+tk.E, pady=1)
    # output
    outportvar = tk.StringVar(root)
    outportlabel = tk.ttk.Label(root, text="OUT:")
    outportlabel.grid(row=1, column=0)
    outportmenu = tk.ttk.OptionMenu(root, outportvar, outports[0], *outports)
    outportmenu.configure(width=len(max(outports, key=len)))
    outportmenu.grid(row=1, column=1, sticky=tk.W+tk.E, pady=1)
    # keys
    keys = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A', 'A#', 'Bb', 'B']
    keyvar = tk.StringVar(root)
    keylabel = tk.ttk.Label(root, text="KEY:")
    keylabel.grid(row=2, column=0)
    keymenu = tk.ttk.OptionMenu(root, keyvar, keys[0],*keys)
    keymenu.grid(row=2, column=1, sticky=tk.W+tk.E, pady=1)
    # scales
    scales = ["major", "minor"]
    scalevar = tk.StringVar(root)
    scalelabel = tk.ttk.Label(root, text="SCALE:")
    scalelabel.grid(row=3, column=0)
    scalemenu = tk.ttk.OptionMenu(root, scalevar, scales[0], *scales)
    scalemenu.grid(row=3, column=1, sticky=tk.W+tk.E, pady=1)
    # apply button
    applybutton = tk.ttk.Button(root, text=" Apply ", width=30, command=lambda: apply(inportvar.get(), outportvar.get(), scalevar.get(), keyvar.get(), inports, outports))
    applybutton.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=1)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(200, backgroundthread)
    tmp = open("favicon.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap("favicon.ico")
    os.remove("favicon.ico")

def runui():
    root.mainloop()