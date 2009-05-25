#!/usr/bin/python
#
# Copyright (C) 2009 Paul W. Frields
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author: Paul W. Frields <stickster@gmail.com>


import pygst
pygst.require('0.10')
import gst
from sys import stdout

class PulseCatcherPipeline:
    def __init__(self, pulseDevice, outfile=stdout):
        self.pipeline = gst.Pipeline('pcPipeline')
        self.source = gst.element_factory_make('pulsesrc', 'source')
        self.source.set_property('device', pulseDevice)
        self.encoder = gst.element_factory_make('vorbisenc', 'encoder')
        self.encoder.set_property('quality', 0.5)
        self.muxer = gst.element_factory_make('oggmux', 'muxer')
        self.sink = gst.element_factory_make('filesink', 'sink')
        self.sink.set_property('location', outfile)

    