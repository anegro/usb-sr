#! /usr/bin/python
#
# USB Sync and Remove (usb-sr)
# A Python based desktop indicator to safely remove USB drives.
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
import subprocess
import pynotify

APP_NAME = 'usb-sr'
ICON_NAME = 'distributor-logo'



# Actions to be taken when pressing certain menu entries
def unmount_clicked(widget, data=None):
	print "Unmounting %s ..." % data
	notify_begin_unmount.show()
	
	part = data
	dev = data.rstrip('1234567890')
	
	subprocess.call('udisksctl unmount --block-device %s' % part, shell=True)
	subprocess.call('udisksctl power-off --block-device %s' % dev, shell=True)

	notify_begin_unmount.close()
	notify_end_unmount.show()


def quit(widget, data=None):
	gtk.main_quit()

def build_menu(indicator):
	# Create menu
	menu = gtk.Menu()

	# Get mounted devices
	mount_devices = subprocess.check_output('mount -l | grep -E ".* on /media/$USER.*" | cut -d " " -f 1', shell=True)
	mount_names = subprocess.check_output('mount -l | grep -E ".* on /media/$USER.*" | grep -E -o "\[.*\]" | tr -d "[]"', shell=True)
	mounts = dict(zip(mount_names.splitlines(), mount_devices.splitlines()))
	
	print mounts ###

	# Add menu elements
	for name in mounts:
		item = gtk.MenuItem(name)
		item.connect("activate", unmount_clicked, mounts[name])
		item.show()
		menu.append(item)
 
	#check = gtk.CheckMenuItem("Check Menu Item")
	#check.show();
	#menu.append(check)

	#radio = gtk.RadioMenuItem(None, "Radio Menu Item")
	#radio.show()
	#menu.append(radio)

	separator = gtk.SeparatorMenuItem()
	separator.show()
	menu.append(separator)

	item_exit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
	item_exit.connect("activate", quit)
	item_exit.show()
	menu.append(item_exit)

	indicator.set_menu(menu)


# Main code
if __name__ == "__main__":

	# Create indicator
	indicator = appindicator.Indicator (APP_NAME, ICON_NAME, appindicator.CATEGORY_APPLICATION_STATUS)
	indicator.set_status (appindicator.STATUS_ACTIVE)

	# Indicator icons
	#ind.set_icon("indicator-messages")
	#ind.set_attention_icon("indicator-messages-new")

	# Set indicator menu
	build_menu(indicator)

	# Create notifications
	if pynotify.init(APP_NAME):
		notify_begin_unmount = pynotify.Notification("Unmounting device", "Please wait...")
		notify_begin_unmount.set_timeout(600)

		notify_end_unmount = pynotify.Notification("Device unmounted", "Now you can safely remove it")
		notify_end_unmount.set_timeout(60)
	else:
		print "there was a problem initializing the pynotify module"

	# Run main code
	gtk.main()
