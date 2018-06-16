# ============================================================================
# FILE: MidiNvim.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import neovim
import os
# (only dependency)
import rtmidi
# Need a separate thread for the MIDI
from threading import Thread
import time

class MidiNvimProgrammer(object):
    def __init__(self):
        pass

class MidiNvim(object):
    """ Main class for the plugin, manages
        the input commands and the spawning of
        explorers """
    def __init__(self, nvim, log=False):
        self.nvim = nvim
        self.midiin = None
        self.mode = "programmer"


# ============================================================================
# Helpers
# ============================================================================
    def thread_midiHandler(self):
        # This is how we do it
        while self.threadShallRun:
            m = self.midiin.getMessage(50) # 50ms timeout
            if m:
                self.nvim.async_call(self.midiHandler, m, "")

    def handProgrammerEvent(self, m):
        # This handler manages the programmer "modes"/"inserts"
        if m.getNoteNumber() == 55:
            self.nvim.command('normal! h')
        elif m.getNoteNumber() == 64:
            self.nvim.command('normal! l')
        elif m.getNoteNumber() == 60:
            self.nvim.command('normal! k')
        elif m.getNoteNumber() == 62:
            self.nvim.command('normal! j')

    # Debug printer
    def print_message(self, midi):
        outStr = ""
        if midi.isNoteOn():
            outStr = 'ON: ' + str(midi.getNoteNumber()) + " " + str(midi.getVelocity())
        elif midi.isNoteOff():
            outStr = 'OFF: ' +  str(midi.getNoteNumber())
        elif midi.isController():
            outStr = 'CONTROLLER' + midi.getControllerNumber() + midi.getControllerValue()
        self.nvim.current.buffer.append(outStr)

# ============================================================================
# Commands
# ============================================================================
    def startMidi(self, args, range):
        if self.midiin == None:
            self.midiin = rtmidi.RtMidiIn()
        if len(args) > 0:
            port = int(args[0])
        else:
            port = 0
        self.midiin.openPort(port)
        # Shall start a background thread
        self.threadShallRun = True
        self.midiThread = Thread(target=self.thread_midiHandler)
        self.midiThread.start()

    def stopMidi(self, args, range):
        # Shall start a background thread
        self.threadShallRun = False

    def listMidiInputs(self, args, range):
        self.midiin = rtmidi.RtMidiIn()
        self.nvim.command('split Midi_Inputs')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=midi_inputs')
        portCount = int(self.midiin.getPortCount())
        self.nvim.current.line="~ Listing " + str(portCount) + " MIDI port(s) ~"
        self.nvim.current.buffer.append("--------------------------")
        i = 0
        while(i < portCount):
            self.nvim.current.buffer.append("%d: %s" % (i, self.midiin.getPortName(i)))
            i += 1

    # Main handler
    # ===========
    def midiHandler(self, args, range):
        m = args
        # This is where the MiGiC shall happen! 
        if self.mode == 'programmer' and m.isNoteOn():
            self.handProgrammerEvent(m)
        else:
            self.print_message(m)
