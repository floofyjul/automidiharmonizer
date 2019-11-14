import rtmidi_python as rtmidi

def initmidiinout():
    global midiout, midiin
    midiout = rtmidi.MidiOut(b'out')
    midiin = rtmidi.MidiIn(b'in')

def getports():
    portsin = midiin.ports
    portsout = midiout.ports
    return portsin, portsout
    # Attempt to open the port

def openports(inport: int, ouport: int):
    """Opens the midi ports.
    
    Returns midiin, midiout"""
    midiin.close_port()
    midiout.close_port()
    midiin.open_port(inport)
    midiout.open_port(ouport)
    return midiin, midiout