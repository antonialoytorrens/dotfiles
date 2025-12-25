#!/usr/bin/env python3
#Name: desktop-session-exit.py
#Version: 2.0
#Depends: python, Gtk
#Author: Dave (david@daveserver.info)
#Purpose: GUI for desktop-session-exit script
#License: gplv3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import gettext
import os
import sys
#Variables
ButtonWidth = 240
ButtonHeight = 80
#Get base icon theme 
icon_theme = Gtk.IconTheme.get_default()

#ICONS = "/usr/share/icons/antiX-numix-bevel"
#ICONS = "/usr/share/icons/antiX-numix-square"
#ICONS = "/usr/share/icons/antiX-papirus"
#ICONS = "/usr/share/icons/antiX-faenza"
#ICONS = "/usr/share/icons/antiX-moka"
ICONS = "/usr/share/icons/antiX-qogir"
#ICONS = "/usr/share/icons/antiX-kora"

gettext.install(domain = "desktop-session-exit")

class mainWindow(Gtk.Window):
    def button_clicked(self, widget, command):
        os.system(command)
        sys.exit()
    
    def get_icon(self,appicon):
        icon_size = 48
        if os.path.isfile(str(appicon)):
            icon = appicon
        elif type(appicon) == str:
            try:
                icon = icon_theme.lookup_icon(appicon, icon_size, 0)
                icon = icon.get_filename()
            except:
                print(_("Cannot get filename for icon based on icon name"))
                
        if not icon:
            print(_("Trying fallback icons"))
            icon_dictionary = {"system-lock-screen": ICONS+"/lock.png", "system-restart-session": ICONS+"/restart.png", "system-reboot": ICONS+"/reboot.png", "system-hibernate": ICONS+"/hibernate.png", "system-log-out": ICONS+"/logout.png", "system-suspend": ICONS+"/suspend.png", "system-shutdown": ICONS+"/shutdown.png"}
            if appicon in icon_dictionary:
                icon = icon_dictionary.get(appicon)
            else:
                print(_("Cannot find icon and fallback does not exist"))
            
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon)
        except:
            print(_("Cannot generate pixbuf from icon %s\n >Setting blank" % icon))
            pixbuf = GdkPixbuf.Pixbuf.new(0,True, 8,icon_size, icon_size)
        
        pixbuf = GdkPixbuf.Pixbuf.scale_simple(pixbuf, icon_size, icon_size,0)
        return pixbuf,icon
    
    def build_button(self,image,text,command,column,row):
        #Increase button count by one for use of mnemonic
        #Uncomment the two below lines for number based key selection
        #self.button_loop += 1
        #button = Gtk.Button.new_with_mnemonic("_"+str(self.button_loop)+" "+_(text))
        #Uncomment the below line for name based key selection
        button = Gtk.Button.new_with_mnemonic("_"+_(text))
        
        icon_info = self.get_icon(image)
        button_image = Gtk.Image.new_from_pixbuf(icon_info[0])
        button.set_image(button_image)
        button.set_image_position(Gtk.PositionType.TOP)
        button.set_always_show_image(True)
        button.connect("clicked", self.button_clicked, command)
        button.set_hexpand(True)
        button.set_vexpand(True)
        button.set_size_request(ButtonWidth, ButtonHeight)
        button.show()
        
        self.grid.attach(button, column, row, 1, 1)

    def keypress(self,window,key):
        #print(key.keyval)
        if key.keyval == 65307:
            Gtk.main_quit()
        if key.state & Gdk.ModifierType.CONTROL_MASK:
            if key.keyval == 113:
                Gtk.main_quit()

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_size_request(400,100)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(_("Exit Session"))
        self.connect("key-press-event", self.keypress)
        self.set_keep_above(True)
        self.stick()
        self.show()
        
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.show()
        
        #Set first button number for use of mnemonic
        self.button_loop = 0
        #Build Buttons: ICON, NAME, ACTION, COLUMN, ROW
        self.build_button("system-lock-screen","Lock Screen","desktop-session-exit -L",1,1)
        self.build_button("system-restart-session","Restart Session","desktop-session-exit -R",1,2) 
        self.build_button("system-reboot","Reboot","desktop-session-exit -r",1,3)
        #self.build_button("system-hibernate","Hibernate","desktop-session-exit -H",1,4)
        self.build_button("system-log-out","Log Out","desktop-session-exit -l",2,1)
        self.build_button("system-suspend","Suspend","desktop-session-exit -S",2,2)
        self.build_button("system-shutdown","Shutdown","desktop-session-exit -s",2,3)
        
win = mainWindow()
win.connect("delete-event", Gtk.main_quit)
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) # without this, Ctrl+C from parent term is ineffectual
Gtk.main()
