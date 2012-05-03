# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# Script copyright (C) 2012 Thomas Achtner (offtools)

import bpy
import sys

try:
	sys.path.append('/usr/lib/python3.2/site-packages')
	import liblo
except ImportError as err:
	print(err, "you need to install pyliblo and set the correct search path in server.py")

class client(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(client, cls).__new__(cls, *args, **kwargs)
		return cls._instance
		
	def __init__(self):
		self.target = liblo.Address(9900)

	def port_getter(self):
		return self.target.port
        
	def port_setter(self, port):
		self.target = liblo.Address(port)

	port = property(port_getter, port_setter)
		
	def quit(self):
		liblo.send(self.target, "/quit")

	def send(self, path, *args):
		liblo.send(self.target, path, *args)
