# ============================================================================
# FILE: MidiNvimProgrammer.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================

class MidiNvimProgrammer(object):
    def __init__(self, nvim, statusBuffer):
        self.statusBuffer = statusBuffer
        self.nvim = nvim

    def handleEvent(self, m):
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

