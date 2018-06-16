# ============================================================================
# FILE: __init__.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

import neovim
from MidiNvim.MidiNvim import MidiNvim


@neovim.plugin
class midiVimHandlers(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.midiNvim = MidiNvim(nvim, log=False)

    @neovim.command("StartMidi", range='', nargs='*', sync=True)
    def startMidi(self, args, range):
        self.midiNvim.startMidi(args, range)

    @neovim.command("StopMidi", range='', nargs='*', sync=True)
    def stopMidi(self, args, range):
        self.midiNvim.stopMidi(args, range)

    @neovim.command("ListMidiInputs", range='', nargs='*', sync=True)
    def listMidiInputs(self, args, range):
        self.midiNvim.listMidiInputs(args, range)


