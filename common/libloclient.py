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
import liblo
from liblo import make_method

class LibloClient(liblo.ServerThread):
	def __init__(self):
		super().__init__()
		self.appHandler = dict()

	@make_method('/shutdown', 's')
	def shutdown(self, path, args, types, source, user_data):
		print ("CLIENT: received server shutdown: ", args)
		self.close()

	@make_method('/srvinfo', 's')
	def srvinfo(self, path, args, types, source, user_data):
		print ("CLIENT: connected - got server reply: ", args)

	@make_method('/error', 's')
	def error(self, path, args, types, source, user_data):
		print ("CLIENT: received error message: ", args)

	@make_method(None, None)
	def fallback(self, path, args, types, source, user_data):
		print ("CLIENT: received unhandled message: ", path, args, types, source.url, user_data)

	def add_apphandler(self, apphandler, func):
		'''register an apphandler, will be activated on connect'''
		if not apphandler in self.appHandler:
			self.appHandler[apphandler] = set()
		self.appHandler[apphandler].add(func)

	def _start_apphandler(self):
		'''activate registered apphandler''' 
		for handler in self.appHandler.keys():
			for func in self.appHandler[handler]:
				getattr(bpy.app.handlers, handler).append(func)

	def _stop_apphandler(self):
		'''deactivate apphandler'''
		for handler in self.appHandler.keys():
			try:
				for func in self.appHandler[handler]:
					getattr(bpy.app.handlers, handler).remove(func)
			except ValueError:
				print("AppHandler %s already removed")

	def connect(self, host, port, proto=liblo.UDP):
		'''connect to a osc server''' 
		print("CLIENT: connecting")

		try:
			self.target = liblo.Address(port)
			liblo.send(self.target, "/connect")
			self.start()
		except liblo.AddressError as err:
			print("TODO Error Handling", err)
			return
			
		self._start_apphandler()

	def send(self, path, *args):
		try:
			super().send(self.target, path, *args)
		except AttributeError:
			print("Not connected - no messages send")

	def receive(self):
		while self.recv(0):
			pass

	def disconnect(self):
		try:
			self.close()
			liblo.send(self.target, "/disconnect")
		except AttributeError:
			pass

	def close(self):
		self._stop_apphandler()
		self.stop()
		try:
			del self.target
		except AttributeError:
			print("Not connected")

__client = LibloClient()

Client = lambda : __client

def register():
	print("client.register")
	pass

def unregister():
	print("client.unregister")
	pass
