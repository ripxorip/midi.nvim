# midi.nvim

MIDI input layer for Neovim

## Introduction
The purpose of this plugin is to be able to input commands/text in to Neovim using
MIDI. Below you can soon see some example of the plugin in action.

## Commands
```vim
" Lists the available MIDI ports
ListMidiInputs
" Start listening to MIDI commands
StartMidi
" Start listening to MIDI commands
StopMidi
```

## Design
The plugin starts its own thread that is used in order to listen to MIDI from the desired port.
When a MIDI message is retrieved, it is handled in the _midiHandler_ method of the main class.

## Installation
**Note:** midi.nvim requires Neovim(latest is recommended) with Python3 enabled.
See [requirements](#requirements) if you aren't sure whether you have this.

For vim-plug:

```vim

call plug#begin()

Plug 'philip-karlsson/midi.nvim', { 'do': ':UpdateRemotePlugins' }

call plug#end()
```

## Requirements
midi.nvim requires Neovim with Python3.
tIf `:echo has("python3")` returns `1`, then you have python 3 support; otherwise, see below.

You can enable the Neovim Python3 interface with pip:

    pip3 install neovim

In order to get MIDI in to python this plugin relies on the [rtmidi python package](https://pypi.org/project/rtmidi/)
, install this with pip:

    pip3 install rtmidi

## Self-Promotion
Like midi.nvim? Make sure to follow the repository and why not leave a star.

## Contributors
- Philip Karlsson


## License
MIT License

Copyright (c) 2018 Philip Karlsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
