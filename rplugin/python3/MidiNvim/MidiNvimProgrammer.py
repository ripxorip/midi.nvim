# ============================================================================
# FILE: MidiNvimProgrammer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import time
import datetime

def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis

class MidiNvimProgrammer(object):
    def __init__(self, nvim, statusBuffer):
        self.statusBuffer = statusBuffer
        self.nvim = nvim
        self.prev = datetime.datetime.now()

    def handleEvent(self, m):
        # This handler shall be rewriten
        if m is not None:
            # New event
            self.prev = datetime.datetime.now()
            mnum = m.getNoteNumber()
            statStr = "Got " + m.getMidiNoteName(mnum) + " " + "(%d)" % (mnum)
            # This handler manages the programmer "modes"/"inserts"
            if m.isNoteOn():
                if m.getNoteNumber() == 55:
                    self.nvim.command('normal! h')
                elif m.getNoteNumber() == 64:
                    self.nvim.command('normal! l')
                elif m.getNoteNumber() == 60:
                    self.nvim.command('normal! k')
                elif m.getNoteNumber() == 62:
                    self.nvim.command('normal! j')
            self.statusBuffer[0] = statStr
        else:
            # Check for time
            if(millis_interval(self.prev, datetime.datetime.now()) > 2000):
                self.statusBuffer[0] = "Waiting for MIDI.."

