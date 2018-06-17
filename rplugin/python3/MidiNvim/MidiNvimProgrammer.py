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
                65: 'normal! h',
                60: 'normal! b',
                74: 'normal! l',
                79: 'normal! w',
                69: 'normal! k',
                71: 'normal! j',
                72: 'normal! <C-d>',
                68: 'normal! <c-u>',
                73: 'normal! i ', # insert space
                75: 'normal! i0 ', # insert number
                76: 'normal! ia ', # insert character
                78: 'normal! i; ', # insert semi-colon
                80: 'normal! o ', # insert new line
                83: 'IncrementChar', # increment char
                81: 'DecrementChar', # decrement char
                82: 'normal! ~h', # Change case
                }
        # List of all keys that can be used to start a melody
        self.melodyKeys = [59, 52]
        # This dictionary contains all melodies that can be played
        self.melodies = {
                'mario': [52, 64, 49, 61, 50, 62],
                'majorArp': [59, 64, 68, 71],
                'dedu': [59, 53],
                }
        # This dictionary contains binding between action and melody
        self.melodyActions = {
                'majorArp': 'insertCReturn',
                'dedu': 'undo',
                'mario': 'guitarsCanCode',
                }

        self.actionImplementations = {
                'moteTwentyCharsDown': 'normal! 20j',
                'insertCInclude': 'normal! i#include ',
                'inserCInt': 'normal! iint ',
                'insertCReturn': 'normal! ireturn ',
                'insertCVoid': 'normal! ivoid ',
                'undo': 'normal! u',
                'guitarsCanCode': 'normal! iGuitars can code \m/ ',
                }

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

    def checkMelodyInArray(self):
        for mel in self.keys.melodies:
            if len(self.melodyArray) >= len(self.keys.melodies[mel]):
                allSame = True
                for idx, note in enumerate(self.keys.melodies[mel]):
                    if self.melodyArray[idx] != self.keys.melodies[mel][idx]:
                        allSame = False
                        break
                if allSame:
                    return True, mel
        return False, None

    def processMidiEvent(self, m):
        mnum = m.getNoteNumber()
        statStr = "Got " + m.getMidiNoteName(mnum) + " " + "(%d)" % (mnum)
        # This handler manages the programmer "modes"/"inserts"
        if m.isNoteOn():
            # Handle single key
            if (m.getNoteNumber() in self.keys.singleKeys) and not self.inMelody:
                cmd = self.keys.singleKeys[m.getNoteNumber()]
                statStr += " | single note cmd: \"%s\"" % cmd
                self.nvim.command(cmd)
            # Handle melodies
            elif (m.getNoteNumber() in self.keys.melodyKeys) or self.inMelody:
                self.inMelody = True
                statStr += " | looking for melody.."
                self.melodyArray.append(m.getNoteNumber())
                ret, foundMel = self.checkMelodyInArray()
                if ret:
                    statStr = " | melody \"%s\" detected, performing action!" % foundMel
                    # Perform the action as stated by the melody
                    self.nvim.command(self.keys.actionImplementations[self.keys.melodyActions[foundMel]])
                    self.melodyArray = []
                    self.inMelody = False
            self.statusBuffer[0] = statStr

    def processTimeEvent(self):
        # Timeout for a command
        if(self.timeSinceLast() > 1000) or (self.timeSinceLast() > 400 and self.inMelody):
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

