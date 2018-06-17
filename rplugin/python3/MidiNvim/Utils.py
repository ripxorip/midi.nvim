# ============================================================================
# FILE: Utils.py
# AUTHOR: Philip Karlsson <philipkarlsson at me.com>
# License: MIT license
# ============================================================================
import neovim
import os

class Utils(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def incrementChar(self, args, range):
        row = self.nvim.current.window.cursor[1]
        ch = self.nvim.current.line[row]
        lineList = list(self.nvim.current.line)
        num = ord(ch)
        num += 1
        ch = chr(num)
        lineList[row] = ch
        self.nvim.current.line = "".join(lineList)

    def decrementChar(self, args, range):
        row = self.nvim.current.window.cursor[1]
        ch = self.nvim.current.line[row]
        lineList = list(self.nvim.current.line)
        num = ord(ch)
        num -= 1
        ch = chr(num)
        lineList[row] = ch
        self.nvim.current.line = "".join(lineList)
