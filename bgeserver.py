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

import bge
import types
import bgehandler
import bgevideotexture
from OSC import OSCServer

class BgeOSCServer(OSCServer):
	def __new__(type, *args):
		if not '_the_instance' in type.__dict__:
			type._the_instance = object.__new__(type)
		return type._the_instance

	def __init__(self, ip="127.0.0.1", port=9900):
		super().__init__((ip,port))
		self.timeout = 0
		self.__module = list()

		self.addMsgHandler('/connect', self.callback_connect)		
		self.addMsgHandler('/debug', bgehandler.debug)
		self.addMsgHandler('/quit', bgehandler.quit)
		self.addMsgHandler('/debug', bgehandler.update_objects)
		self.addMsgHandler("/data/objects", bgehandler.update_objects)
		self.addMsgHandler("/data/object/scaling", bgehandler.update_object_scaling)
		self.addMsgHandler("/data/object/color", bgehandler.update_object_color)
		self.addMsgHandler("/data/camera", bgehandler.update_camera)
		self.addMsgHandler("/data/light", bgehandler.update_light)
		self.addMsgHandler("/data/light/normal", bgehandler.update_light_normal)
		self.addMsgHandler("/data/light/spot", bgehandler.update_light_spot)
		self.addMsgHandler("/data/light/sun", bgehandler.update_light_sun)			
		self.addMsgHandler("/data/objects/polygon", bgehandler.update_mesh)
		self.addMsgHandler("/scene", bgehandler.change_scene)

		vtex = bgevideotexture.videotexture()
		self._addUpdateModule(vtex)
		self.addMsgHandler("/texture/state", vtex.state)
		self.addMsgHandler("/texture/movie", vtex.movie)
		self.addMsgHandler("/texture/camera", vtex.camera)
			
	def handle_timeout(self):
		self.timed_out = True
		
	def _addUpdateModule(self, instance):
		if hasattr(instance, 'update'):
			if type(instance.update) in (types.FunctionType, types.MethodType):
				self.__module.append(instance)
		
	def callback_connect(self, path, tags, args, source):
		print('receiving connect: ', path, tags, args, source)
		
	def update(self):
		self.timed_out = False
		while not self.timed_out:
			self.handle_request()

		for mod in self.__module:
			mod.update()
