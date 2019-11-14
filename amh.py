import time
import rtmidi_python as rtmidi

midiout = rtmidi.MidiOut(b'out')
midiin = rtmidi.MidiIn(b'in')
available_ports = midiout.ports
available_ports2 = midiin.ports

#list the available ports
print("available inputs")
print(available_ports2)
print("availabe outputs")
print(available_ports)

# Attempt to open the port
if available_ports2:
    midiin.open_port(0)
else:
    midiin.open_virtual_port("My virtual input")
# Attempt to open the port
if available_ports:
    midiout.open_port(3)
else:
    midiout.open_virtual_port("My virtual output")

print("poop")

keymap = {
    "c": 0,
    "c#": 1,
    "db": 1,
    "d": 2,
    "d#": 3,
    "eb": 3,
    "e": 4,
    "f": 5,
    "f#": 6,
    "gb": 6,
    "g": 7,
    "g#": 8,
    "ab": 8,
    "a": 9,
    "a#": 10,
    "bb": 10,
    "b": 11
}

minormap = {
    0:0,
    1:1,
    2:2,
    3:3,
    4:3,
    5:5,
    6:6,
    7:7,
    8:8,
    9:8,
    10:10,
    11:10
}

def harmonize(pitch, scale, key):
    note = pitch % 12
    octave = pitch // 12
    if scale == "minor":
        note = minormap[note]
    if scale == "major":
        pass
    note = note + keymap[key]
    pitch = note + 12 * octave
    return pitch

while True:
    midiag = midiin.get_message()
    if midiag != (None, None):
        print(midiag)
        status, pitch, velocity = midiag[0]
        pitch = harmonize(pitch, "major", "bb")
        midiout.send_message([status, pitch, velocity])
        # midiout.send_message(midiag[0][0], pitch, midiag[0][2]])
        
# note_on = [0x90, 60, 112]
# note_off = [0x80, 60, 0]
# midiout.send_message(note_on)
# time.sleep(2)
# I tried running the script without having to invoke the sleep function but it doesn't work.
# If someone could enlighten me as to why this is, I'd be more than grateful.
# midiout.send_message(note_off)
del midiout