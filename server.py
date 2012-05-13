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

try:
	sys.path.append('/usr/lib/python3.2/site-packages')
	import liblo
except ImportError as err:
	print(err, "you need to install pyliblo and set the correct search path in client.py")

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
		
		#	all objects: recv name, location, rotation_euler
		self.add_method("/data/objects", "sffffff", self.update_objects)

		#	object: recv name, scale, objectcolor		
		self.add_method("/data/object", "sfffffff", self.update_object)
		
		#	camera: rcv name, lens, ortho_scale, near, far, perspective, shift_x, shift_y
		self.add_method("/data/camera", "sffffiff", self.update_camera)
				
		self.add_method("/data/objects/polygon", "siifff", self.update_mesh)
		self.add_method("/data/camera", "ff", self.not_implemented)        
		self.add_method("/data/scene", "", self.not_implemented)
		self.add_method("/texture/state", "ss", self.modules[videotexture].state)
		self.add_method("/texture/movie", "sss", self.modules[videotexture].movie)
		self.add_method("/texture/camera", "sssiii", self.modules[videotexture].camera)
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

		#	lens shift
#		camera = bge.logic.getCurrentScene().active_camera
#		sx = sy = 0
#		if hasattr(camera, "shift_x"):
#			print("shift x", camera.shift_x)
#			sx = camera[shift_x]
#		if hasattr(camera, "shift_y"):
#			print("shift y", camera.shift_y)
#			sy = camera[shift_y]

#		pmatrix = camera.projection_matrix

#		pmatrix[2][0] = 0
#		pmatrix[2][1] = 0
#		camera.projection_matrix = pmatrix

	def update_objects(self, path, args):
		scene = bge.logic.getCurrentScene()
		_id = args[0]
		ob = scene.objects[_id]
		ob.position = (args[1],args[2],args[3])
		ob.orientation = (args[4],args[5],args[6])

	def update_object(self, path, args):
		scene = bge.logic.getCurrentScene()
		_id = args[0]
		ob = scene.objects[_id]
		ob.scaling = (args[1],args[2],args[3])
		ob.color = (args[4],args[5],args[6],args[7])
		
	def update_camera(self, path, args):
		# name, lens, ortho_scale, near, far, perspective, shift_x, shift_y
		scene = bge.logic.getCurrentScene()
		camera =  scene.cameras[args[0]]

		camera.lens = float(args[1])
		camera.ortho_scale = float(args[2])
		camera.near = float(args[3])
		camera.far = float(args[4])
		camera.perspective = float(args[5])
		camera["shift_x"] = float(args[6])
		camera["shift_y"] = float(args[7])
#		pmatrix = camera.projection_matrix

#		pmatrix[2][0] = 2*shift_x
#		pmatrix[2][1] = 2*shift_y
#		camera.projection_matrix = pmatrix

	def update_mesh(self, path, args):
		scene = bge.logic.getCurrentScene()
		ob = scene.objects[args[0]]
		polygon_index = args[1]
		vertex_index = args[2]
		x = args[3]
		y = args[4]
		z = args[5]

		#	retrieve polygon
		polygon = ob.meshes[0].getPolygon(polygon_index)
		
		#	get verts from polygon
		verts = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
		if verts[3] == 0: verts.pop()

		#	get material index (workaround for matid bug, matid is not an attr of KX_PolyProxy)
		mat_index = ob.meshes[0].materials.index(polygon.material)
		mesh = ob.meshes[0]
		try:
			vertex = mesh.getVertex(mat_index, verts[vertex_index])
			vertex.setXYZ([x,y,z])
		except IndexError as err:
			print("%s : mat_idx: %d vert_idx: %d" %(err, mat_index, vertex_index))
								 
	def not_implemented(self, path, args):
		print("not implemented: ", path, args)

	def fallback(self, path, args):
		print('no handler for path: ', path, args)
