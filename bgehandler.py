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

def debug(path, tags, args, source):
	print(path, tags, args, source)
	
def quit(path, tags, args, source):
	print(path, tags, args, source)

def update_objects(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	_id = args[0]
	ob = scene.objects[_id]
	ob.position = (args[1],args[2],args[3])
	ob.orientation = (args[4],args[5],args[6])

def update_object_scaling(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	_id = args[0]
	ob = scene.objects[_id]
	ob.scaling = (args[1],args[2],args[3])

def update_object_color(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	_id = args[0]
	ob = scene.objects[_id]
	ob.color = (args[1],args[2],args[3],args[4])
	
def update_camera(path, tags, args, source):

	scene = bge.logic.getCurrentScene()
	camera =  scene.cameras[args[0]]

	angle = args[1]
	aspect = args[2]
#		camera.lens = lens
#		camera.ortho_scale = args[3]
#		camera.near = args[4]
#		camera.far = args[5]
#		camera.perspective = args[6]

	projection_matrix = camera.projection_matrix

	e = 1.0/math.tan(angle/2.0)

	shift_x = args[7]
	shift_y = args[8]

	projection_matrix[0][0] = e
	projection_matrix[1][1] = e/aspect
	
	projection_matrix[0][2] = 2*shift_x
	projection_matrix[1][2] = 2*shift_y
	
	camera.projection_matrix = projection_matrix

def update_light(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	light = scene.objects[args[0]]
	light.energy = args[1]
	light.color = (args[2], args[3], args[4])
	light.spotblend = float(0)

def update_light_normal(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	light = scene.objects[args[0]]
	light.type = 2
	light.distance = args[1]
	light.lin_attenuation = args[2]
	light.quad_attenuation = args[3]
	
def update_light_spot(path, tags, args, source):
	print(path, args)
	scene = bge.logic.getCurrentScene()
	light = scene.objects[args[0]]
	light.type = 0
	light.distance = args[1]
	light.lin_attenuation = args[2]
	light.quad_attenuation = args[3]
	light.spotsize = args[4]
	light.spotblend = args[5]
	
def update_light_sun(path, tags, args, source):
	scene = bge.logic.getCurrentScene()
	light = scene.objects[args[0]]
	light.type = 1
	
def update_mesh(path, tags, args, source):
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

def change_scene(path, tags, args, source):
	name = args[0]
	scene = bge.logic.getCurrentScene()
	scene.replace(name)
