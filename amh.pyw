import time
from source import porthandler
from source.ui import _uisetup, runui

if __name__ == "__main__":
    porthandler.initmidiinout()
    inports, outports = porthandler.getports()
    _uisetup(inports, outports)
    runui()

