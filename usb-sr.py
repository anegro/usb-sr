#! /usr/bin/python
#
# USB Sync and Remove (usb-sr)
# An Python based desktop indicator to safely remove USB drives.
#
# (c) 2016 Antonio Negro
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License v3.0 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License v3.0 for more details.
#
# You should have received a copy of the GNU General Public License v3.0
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Instructions:
#
# 1. Copy this file to /usr/local/bin
# 2. Launch it, or better yet, add it to startup programs list so it runs on login.

import gobject
import gtk
import appindicator
import os

APPINDICATOR_ID = 'usb-sr'
ICON_NAME = 'distributor-logo'

# Actions to be taken when pressing certain menu entries
def action1_clicked(widget, data=None):
    print "Lanzando gedit..."
    os.system("gedit &")

def quit(widget, data=None):
    gtk.main_quit()

# Main code
if __name__ == "__main__":

    # Create indicator
    indicator = appindicator.Indicator (APPINDICATOR_ID, ICON_NAME, appindicator.CATEGORY_APPLICATION_STATUS)
    indicator.set_status (appindicator.STATUS_ACTIVE)

    # Indicator icons
    #ind.set_icon("indicator-messages")
    #ind.set_attention_icon("indicator-messages-new")

    # Create menu
    menu = gtk.Menu()

    # Add menu elements
    item = gtk.MenuItem("Launch GEDIT...")
    item.connect("activate", action1_clicked)
    item.show()
    menu.append(item)
 
    check = gtk.CheckMenuItem("Check Menu Item")
    check.show();
    menu.append(check)

    radio = gtk.RadioMenuItem(None, "Radio Menu Item")
    radio.show()
    menu.append(radio)

    separator = gtk.SeparatorMenuItem()
    separator.show()
    menu.append(separator)

    item_exit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    item_exit.connect("activate", quit)
    item_exit.show()
    menu.append(item_exit)

    # Set indicator menu
    indicator.set_menu(menu)

    # Run main code
    gtk.main()
