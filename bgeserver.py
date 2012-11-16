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
				print("%s update added"%str(instance))
				self.__module.append(instance)
		
	def update(self):
		self.timed_out = False
		while not self.timed_out:
			self.handle_request()

		for mod in self.__module:
			mod.update()

# ##### PyLiblo implementation #####

#~ import sys
#~ 
#~ try:
	#~ sys.path.append('/usr/lib/python3.2/site-packages')
	#~ import liblo
#~ except ImportError as err:
	#~ print(err, "you need to install pyliblo and set the correct search path in client.py")
#~ 
#~ import bge
#~ import math
#~ import main
#~ 
#~ from videotexture import videotexture
#~ 
#~ '''
#~ simple osc server
#~ '''
#~ 
#~ class server(liblo.Server):
	#~ def __init__(self, port):
		#~ liblo.Server.__init__(self, port)
#~ 
		#~ self.modules = dict()
		#~ self.register_module(videotexture)
#~ #		self.register_method(videotexture, "state", "/texture/state", "ss")
#~ #		self.register_method(videotexture, "movie", "/texture/movie", "sss")
#~ #		self.register_method(videotexture, "camera", "/texture/camera", "sss")
#~ 
		#~ self.add_method(str('/debug'), 's', self.debug)
		#~ self.add_method(str('/quit'), '', self.disconnect)
		#~ 
		#~ #	all objects: recv name, location, rotation_euler
		#~ self.add_method("/data/objects", "sffffff", self.update_objects)
#~ 
		#~ #	object: recv name, scaling		
		#~ self.add_method("/data/object/scaling", "sfff", self.update_object_scaling)
#~ 
		#~ #	object: recv name, scale, objectcolor		
		#~ self.add_method("/data/object/color", "sffff", self.update_object_color)
		#~ 
		#~ #	camera: rcv name, lens, ortho_scale, near, far, perspective, shift_x, shift_y
		#~ self.add_method("/data/camera", "sfffffiff", self.update_camera)
		#~ 
		#~ #	light: rcv energy, color
		#~ self.add_method("/data/light", "sffff", self.update_light)
#~ 
		#~ #	normal light: rcv distance, linear_attenuation, quadric_attenuation
		#~ self.add_method("/data/light/normal", "sfff", self.update_light_normal)
#~ 
		#~ #	spot light: rcv distance, linear_attenuation, quadric_attenuation, spot_size, spot_blend
		#~ self.add_method("/data/light/spot", "sfffff", self.update_light_spot)
		#~ 
		#~ #	sun light: rcv name
		#~ self.add_method("/data/light/sun", "s", self.update_light_sun)
		#~ 
		#~ self.add_method("/data/objects/polygon", "siifff", self.update_mesh)
		#~ self.add_method("/data/scene", "", self.not_implemented)
		#~ self.add_method("/texture/state", "sss", self.modules[videotexture].state)
		#~ self.add_method("/texture/movie", "sssi", self.modules[videotexture].movie)
		#~ self.add_method("/texture/camera", "sssiii", self.modules[videotexture].camera)
		#~ 
		#~ #	change scene: rcv name
		#~ self.add_method("/scene", "s", self.change_scene)
		#~ 
		#~ self.add_method(None, None, self.fallback)
#~ 
	#~ def register_module(self, cls):
		#~ if not cls in self.modules:
			#~ self.modules[cls] = cls()
#~ 
#~ #	def register_method(self, cls, attr, path, args):
#~ #		if cls in self.modules:
#~ #			func = getattr(self.modules[cls], attr)
#~ #			self.add_method(path, args, func)
#~ 
	#~ def debug(self, path, args):
		#~ print("Debug Msg: ", args[0])
#~ 
	#~ def disconnect(self, path, args):
		#~ main.stop()
#~ 
	#~ def update(self):
#~ 
		#~ ret = self.recv(0)
		#~ while ret == True:
			#~ ret = self.recv(0)
#~ 
		#~ for i in self.modules:
			#~ self.modules[i].update()
#~ 
	#~ def update_objects(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ _id = args[0]
		#~ ob = scene.objects[_id]
		#~ ob.position = (args[1],args[2],args[3])
		#~ ob.orientation = (args[4],args[5],args[6])
#~ 
	#~ def update_object_scaling(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ _id = args[0]
		#~ ob = scene.objects[_id]
		#~ ob.scaling = (args[1],args[2],args[3])
#~ 
	#~ def update_object_color(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ _id = args[0]
		#~ ob = scene.objects[_id]
		#~ ob.color = (args[1],args[2],args[3],args[4])
		#~ 
	#~ def update_camera(self, path, args):
#~ 
		#~ scene = bge.logic.getCurrentScene()
		#~ camera =  scene.cameras[args[0]]
#~ 
		#~ angle = args[1]
		#~ aspect = args[2]
#~ #		camera.lens = lens
#~ #		camera.ortho_scale = args[3]
#~ #		camera.near = args[4]
#~ #		camera.far = args[5]
#~ #		camera.perspective = args[6]
#~ 
		#~ projection_matrix = camera.projection_matrix
#~ 
		#~ e = 1.0/math.tan(angle/2.0)
#~ 
		#~ shift_x = args[7]
		#~ shift_y = args[8]
#~ 
		#~ projection_matrix[0][0] = e
		#~ projection_matrix[1][1] = e/aspect
		#~ 
		#~ projection_matrix[0][2] = 2*shift_x
		#~ projection_matrix[1][2] = 2*shift_y
		#~ 
		#~ camera.projection_matrix = projection_matrix
#~ 
	#~ def update_light(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ light = scene.objects[args[0]]
		#~ light.energy = args[1]
		#~ light.color = (args[2], args[3], args[4])
		#~ light.spotblend = float(0)
#~ 
	#~ def update_light_normal(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ light = scene.objects[args[0]]
		#~ light.type = 2
		#~ light.distance = args[1]
		#~ light.lin_attenuation = args[2]
		#~ light.quad_attenuation = args[3]
		#~ 
	#~ def update_light_spot(self, path, args):
		#~ print(path, args)
		#~ scene = bge.logic.getCurrentScene()
		#~ light = scene.objects[args[0]]
		#~ light.type = 0
		#~ light.distance = args[1]
		#~ light.lin_attenuation = args[2]
		#~ light.quad_attenuation = args[3]
		#~ light.spotsize = args[4]
		#~ light.spotblend = args[5]
		#~ 
	#~ def update_light_sun(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ light = scene.objects[args[0]]
		#~ light.type = 1
		#~ 
	#~ def update_mesh(self, path, args):
		#~ scene = bge.logic.getCurrentScene()
		#~ ob = scene.objects[args[0]]
		#~ polygon_index = args[1]
		#~ vertex_index = args[2]
		#~ x = args[3]
		#~ y = args[4]
		#~ z = args[5]
#~ 
		#~ #	retrieve polygon
		#~ polygon = ob.meshes[0].getPolygon(polygon_index)
		#~ 
		#~ #	get verts from polygon
		#~ verts = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
		#~ if verts[3] == 0: verts.pop()
#~ 
		#~ #	get material index (workaround for matid bug, matid is not an attr of KX_PolyProxy)
		#~ mat_index = ob.meshes[0].materials.index(polygon.material)
		#~ mesh = ob.meshes[0]
		#~ try:
			#~ vertex = mesh.getVertex(mat_index, verts[vertex_index])
			#~ vertex.setXYZ([x,y,z])
		#~ except IndexError as err:
			#~ print("%s : mat_idx: %d vert_idx: %d" %(err, mat_index, vertex_index))
#~ 
	#~ def change_scene(self, path, args):
		#~ name = args[0]
		#~ scene = bge.logic.getCurrentScene()
		#~ scene.replace(name)
				 #~ 
	#~ def not_implemented(self, path, args):
		#~ print("not implemented: ", path, args)
#~ 
	#~ def fallback(self, path, args):
		#~ print('no handler for path: ', path, args)
