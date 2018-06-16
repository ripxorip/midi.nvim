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
from MidiNvim.MidiNvimProgrammer import MidiNvimProgrammer

class MidiNvim(object):
    """ Main class for the plugin """
    def __init__(self, nvim, log=False):
        self.nvim = nvim
        self.midiin = None
        # Shall be parameter
        self.mode = "programmer"

# ============================================================================
# Helpers
# ============================================================================
    def thread_midiHandler(self):
        # This is how we do it
        while self.threadShallRun:
            m = self.midiin.getMessage(50) # 50ms timeout
            if m:
                self.nvim.async_call(self.handleEvent, m, "")

    def handleEvent(self, args, range):
        m = args
        self.handler.handleEvent(m)

# ============================================================================
# Commands
# ============================================================================
    def startMidi(self, args, range):
        self.ogBuffer = self.nvim.current.buffer
        # Start the status window
        self.nvim.command('split')
        self.nvim.command('wincmd j')
        self.nvim.command('e midi_status')
        self.nvim.current.window.height = 2
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal filetype=midi_status')
        self.statusBufferNumber = self.nvim.current.buffer.number
        self.statusBuffer = self.nvim.current.buffer
        self.nvim.command('wincmd k')
        self.nvim.current.buffer = self.ogBuffer
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
        # Setup hander depending on the preset
        if self.mode == "programmer":
            self.handler = MidiNvimProgrammer(self.nvim, self.statusBuffer)
        #
        initialStatStr = "| Port \"" + self.midiin.getPortName(port)
        initialStatStr += "\" opened, waiting for MIDI..."
        self.statusBuffer[0] = initialStatStr 
        # Always start in normal mode
        self.statusBuffer.append("| Mode: \"%s\" | Preset: \"%s\"" % ("normal", self.mode))

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

