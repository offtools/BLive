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

#
# --- BLive OSC Client, used by blender:
#
# --- OSC Messages are send via Operators, with prefix "BLive_OT_osc_"
# --- These operators are defined in ops.py in the different module subfolders

from . import OSC
from .OSC import OSCClient, OSCMessage, OSCServer

class BLiveClient(OSCClient):
	def __new__(type, *args):
		if not '_instance' in type.__dict__:
			type._instance = object.__new__(type)
		return type._instance

	def __init__(self, server=None):
		if not '_init' in dir(self):
			super().__init__(server)
			self._init = True

	def quit(self):
		if self.address():
			super().send(OSCMessage("/quit"))
			self.close()

	def set_server(self, server):
		if not isinstance(server, OSCServer):
			raise TypeError
		super().set_server(server)

	def addMsgHandler(self, path, callback):
		self.server.addMsgHandler( path, callback )

	def connect(self, ip, port):
		super().connect((ip,port))
		self.send('/connect')

	def send(self, path, *args):
		if self.address():
			try:
				super().send(OSCMessage(path, args))
			except ConnectionRefusedError as err:
				print('[BLive] - connection to server lost')
				self.close()
			except TypeError:
				print('[BLive] - connection to server lost')
				self.close()

def register():
	print("client.register")
	pass

def unregister():
	print("client.unregister")
	pass
