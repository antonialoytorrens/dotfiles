#!/usr/bin/env python
#Name: desktop-session-exit.py
#Version: 2.0
#Depends: python, Gtk
#Author: Dave (david@daveserver.info)
#Purpose: GUI for desktop-session-exit script
#License: gplv3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib, Gio, GdkPixbuf
import gettext
import os
import sys
#Variables
ButtonWidth = 150
ButtonHeight = 120

#ICONS = "/usr/share/icons/antiX-numix-bevel"
#ICONS = "/usr/share/icons/antiX-numix-square"
#ICONS = "/usr/share/icons/antiX-papirus"
#ICONS = "/usr/share/icons/antiX-faenza"
#ICONS = "/usr/share/icons/antiX-moka"
ICONS = "/usr/share/icons/antiX-qogir"
#ICONS = "/usr/share/icons/antiX-kora"

gettext.install(domain = "desktop-session-startup-window")

class mainWindow(Gtk.Window):
    def button_clicked(self, widget, command):
        os.system(command)
        sys.exit()
        
    def build_button(self,image,text,command,column,row):
        #Increase button count by one for use of mnemonic
        self.button_loop += 1
        
        button = Gtk.Button.new_with_mnemonic("_"+str(self.button_loop)+": "+_(text))
        button_image = Gtk.Image.new_from_file(image)
        button.set_image(button_image)
        button.set_always_show_image(True)
        button.connect("clicked", self.button_clicked, command)
        button.set_hexpand(True)
        button.set_vexpand(True)
        button.set_alignment(0.1,0.5)
        button.set_size_request(ButtonWidth, ButtonHeight)
        button.show()

        self.grid.attach(button, column, row, 1, 1)
    
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_size_request(640,480)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(_("Welcome"))
        self.stick()
        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.show()
        
        mainbox = Gtk.VBox()
        self.add(mainbox)
        mainbox.show()
        
        self.grid = Gtk.Grid()
        mainbox.pack_start(self.grid,0,0,1)
        self.grid.show()
        
        #Set first button number for use of mnemonic
        self.button_loop = 0
        #Build Buttons: ICON, NAME, ACTION, COLUMN, ROW
        self.build_button(ICONS+"/docs.png","View Docs","desktop-defaults-run -b file:///usr/share/antiX/FAQ/index.html",1,1)
        self.build_button(ICONS+"/control_centre.png","Control Centre","antixcc.sh",2,1)
        
        exit_button = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
        exit_button.connect("clicked", Gtk.main_quit)
        exit_button.set_size_request(100,75)
        mainbox.pack_start(exit_button, 0,0,1)
        exit_button.show()
        
win = mainWindow()
win.connect("delete-event", Gtk.main_quit)
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) # without this, Ctrl+C from parent term is ineffectual
Gtk.main()
