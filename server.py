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

import sys
sys.path.append('/usr/lib/python3.2/site-packages')
import liblo

import bge
import main
from videotexture import videotexture

'''
simple osc server
'''

class server(liblo.Server):
	def __init__(self, port):
		liblo.Server.__init__(self, port)

		self.modules = dict()
		self.register_module(videotexture)
#		self.register_method(videotexture, "state", "/texture/state", "ss")
#		self.register_method(videotexture, "movie", "/texture/movie", "sss")
#		self.register_method(videotexture, "camera", "/texture/camera", "sss")

		self.add_method(str('/debug'), 's', self.debug)
		self.add_method(str('/quit'), '', self.disconnect)
		self.add_method("/data/objects", "sfffffffffffff", self.update_object)
		self.add_method("/data/objects/vertex", "siifff", self.update_mesh)
		self.add_method("/data/camera", "ff", self.not_implemented)        
		self.add_method("/data/scene", "", self.not_implemented)
		self.add_method("/texture/state", "ss", self.modules[videotexture].state)
		self.add_method("/texture/movie", "sss", self.modules[videotexture].movie)
		self.add_method("/texture/camera", "sss", self.modules[videotexture].camera)
		self.add_method(None, None, self.fallback)

	def register_module(self, cls):
		if not cls in self.modules:
			self.modules[cls] = cls()

#	def register_method(self, cls, attr, path, args):
#		if cls in self.modules:
#			func = getattr(self.modules[cls], attr)
#			self.add_method(path, args, func)

	def debug(self, path, args):
		print("Debug Msg: ", args[0])

	def disconnect(self, path, args):
		main.stop()

	def update(self):

		ret = self.recv(0)
		while ret == True:
			ret = self.recv(0)

		for i in self.modules:
			self.modules[i].update()
#		bge.logic.videotexture.update()

	def update_object(self, path, args):
		scene = bge.logic.getCurrentScene()
		_id = args[0]
		ob = scene.objects[_id]
		ob.position = (args[1],args[2],args[3])
		ob.scaling = (args[4],args[5],args[6])
		ob.orientation = (args[7],args[8],args[9])
		ob.color = (args[10],args[11],args[12],args[13])

	def update_mesh(self, path, args):
		scene = bge.logic.getCurrentScene()
		ob = scene.objects[args[0]]
		m_index = args[1]
		v_index = args[2]
		x = args[3]
		y = args[4]
		z = args[5]

		ob.meshes[0].getVertex(m_index, v_index).setXYZ([ args[3], args[4], args[5] ])


	def not_implemented(self, path, args):
		print("not implemented: ", path, args)

	def fallback(self, path, args):
		print('no handler for path: ', path, args)
