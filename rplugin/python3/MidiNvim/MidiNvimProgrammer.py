# ============================================================================
# FILE: MidiNvimProgrammer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import time
import datetime

# Data structures for keys
class keyBinding(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.singleKeys = {
                55: 'normal! h',
                64: 'normal! l',
                60: 'normal! k',
                62: 'normal! j'
                }
        # List of all keys that can be used to start a melody
        self.melodyKeys = [66]
        # This dictionary contains all melodies that can be played
        self.melodies = {
                'minorInterval': [66, 68, 69]
                }
        # This dictionary contains binding between action and melody
        self.melodyActions = {
                'minorInterval': self.moveTwentyCharsDown
                }

    def moveTwentyCharsDown(self):
        self.nvim.command('normal! 20j')


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
        self.keys = keyBinding(nvim)
        self.inMelody = False
        self.melodyArray = []

    def timeSinceLast(self):
        return millis_interval(self.prev, datetime.datetime.now()) 

    def checkMelodyInArray(self, mel):
        for mel in self.keys.melodies:
            if len(self.melodyArray) >= len(self.keys.melodies[mel]):
                allSame = True
                for idx, note in enumerate(self.keys.melodies[mel]):
                    if self.melodyArray[idx] != self.keys.melodies[mel][idx]:
                        allSame = False
                        break
                if allSame:
                    return True
        return False

    def processMidiEvent(self, m):
        mnum = m.getNoteNumber()
        statStr = "Got " + m.getMidiNoteName(mnum) + " " + "(%d)" % (mnum)
        # This handler manages the programmer "modes"/"inserts"
        if m.isNoteOn():
            # Handle single key
            if m.getNoteNumber() in self.keys.singleKeys:
                cmd = self.keys.singleKeys[m.getNoteNumber()]
                statStr += " | single note cmd: \"%s\"" % cmd
                self.nvim.command(cmd)
            # Handle melodies
            elif (m.getNoteNumber() in self.keys.melodyKeys) or self.inMelody:
                self.inMelody = True
                statStr += " | looking for melody.."
                self.melodyArray.append(m.getNoteNumber())
                for mel in self.keys.melodies:
                    if self.checkMelodyInArray(mel):
                        statStr = " | melody \"%s\" detected, performing action!" % mel
                        # Perform the action as stated by the melody
                        self.keys.melodyActions[mel]()
                        self.melodyArray = []
                        self.inMelody = False
            self.statusBuffer[0] = statStr

    def processTimeEvent(self):
        # Timeout for a command
        if(self.timeSinceLast() > 1000):
            self.inMelody = False
            self.melodyArray = []
            self.statusBuffer[0] = "Waiting for MIDI.."

    def handleEvent(self, m):
        # This handler shall be rewriten
        if m is not None:
            # New MIDI event
            self.prev = datetime.datetime.now()
            self.processMidiEvent(m)
        else:
            # Process time event
            self.processTimeEvent()

