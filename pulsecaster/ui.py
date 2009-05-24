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


import gtk
import gtk.glade
from config import *
from pulseaudio.PulseObj import PulseObj
import os

# FIXME
fname = os.getcwd() + '/data/pulsecaster-prefs-glade.glade'
logofile = os.getcwd() + '/data/icons/scalable/pulsecaster.svg'

class PulseCatcherUI:
    def __init__(self, runlib=True):
        self.xml = gtk.glade.XML(fname)
        self.logo = gtk.gdk.pixbuf_new_from_file(logofile)
        
        # Main dialog basics
        self.main = self.xml.get_widget('main_dialog')
        self.main.set_title('%s %s' % (NAME, VERSION))
        self.main_title = self.xml.get_widget('main_title')
        self.main_title.set_label('<big><big><big><b><i>' +
                                  NAME + '</i></b></big></big></big>')
        self.main.connect('delete_event', self.on_close)
        self.about_button = self.xml.get_widget('about_button')
        self.about_button.connect('clicked', self.showAbout)
        self.close = self.xml.get_widget('close_button')
        self.close.connect('clicked', self.on_close)
        
        # ComboBox setup
        self.user_vox = self.xml.get_widget('user_vox')
        self.subject_vox = self.xml.get_widget('subject_vox')
        self.user_vox = gtk.combo_box_new_text()
        self.subject_vox = gtk.combo_box_new_text()
        self.user_vox.append_text('foo')
        self.user_vox.append_text('bar')
        self.user_vox.set_active(0)

        # About dialog basics
        self.about = self.xml.get_widget('about_dialog')
        self.about.connect('delete_event', self.hideAbout)
        self.about.connect('response', self.hideAbout)
        self.about.set_name(NAME)
        self.about.set_version(VERSION)
        self.about.set_copyright(COPYRIGHT)
        self.about.set_comments(DESCRIPTION)
        self.about.set_license(LICENSE_TEXT)
        self.about.set_website(URL)
        self.about.set_website_label(URL)
        self.authors = [AUTHOR + ' <' + AUTHOR_EMAIL + '>']
        for contrib in CONTRIBUTORS:
            self.authors.append(contrib)
        self.about.set_authors(self.authors)
        self.about.set_logo(self.logo)
        self.about.set_program_name('%s %s' % (NAME, VERSION))

        # Populate PulseAudio sources and sink monitors
        self.pa = PulseObj()
        self.sources = self.pa.pulse_source_list()
        # Create and populate combo boxes
        self.user_vox = gtk.combo_box_new_text()
        self.subject_vox = gtk.combo_box_new_text()
        for source in self.sources:
            if source.monitor_of_sink_name == None:
                self.user_vox.append_text(source.description)
            else:
                self.subject_vox.append_text(source.description)

        self.combo_vbox = self.xml.get_widget('combo_vbox')
        self.combo_vbox.add(self.user_vox)
        self.user_vox.set_active(0)
        self.combo_vbox.add(self.subject_vox)
        self.subject_vox.set_active(0)
        self.combo_vbox.reorder_child(self.user_vox, 0)
        self.combo_vbox.reorder_child(self.subject_vox, 1)
        

        self.combo_vbox.show_all()

        if not runlib:
            self.main.show_all()
            gtk.main()
        

    def on_close(self, *args):
        try:
            self.pa.disconnect()
        except:
            pass
        gtk.main_quit()

    def showAbout(self, *args):
        self.about.show()

    def hideAbout(self, *args):
        self.about.hide()


if __name__ == '__main__':
    pulseCatcher = PulseCatcherUI(False)