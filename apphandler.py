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

# TODO: clean this apphandler mess and merge it into common folder

import bpy
import bmesh
from bpy.app.handlers import persistent
from .client import BLiveClient

@persistent
def scene_update_post_handler(scene):
	for ob in scene.objects:
		if ob.is_updated:
			#~ print("object %s updated" %ob)
			pass
		if ob.is_updated_data:
			#print("object updated data %s updated" %ob)
			pass
			
	for ob in bpy.data.materials:
		if ob.is_updated:
			#~ print("material %s updated" %ob)
			pass
		if ob.is_updated_data:
			#~ print("material updated data %s updated" %ob)
			pass

	#TODO: move all mesh handler here
	for mesh in bpy.data.meshes:
		if mesh.is_updated:
			#print("mesh %s updated" %mesh)
			pass
		if mesh.is_updated_data:
			#print("mesh updated data %s updated" %mesh)
			pass
			
	#	ob color workaround (can't check update of this value')
	#~ for ob in scene.objects:
		#~ if ob.type == 'MESH':
			#~ BLiveClient().send("/data/object/color", [ob.name, ob.color[0], ob.color[1], ob.color[2], ob.color[3]])

	for ob in scene.objects:
		if ob.is_updated:
			BLiveClient().send("/data/objects", [ob.name, ob.location[0], ob.location[1], ob.location[2], ob.rotation_euler[0], ob.rotation_euler[1], ob.rotation_euler[2]])

			if ob.type == 'MESH':
				BLiveClient().send("/data/object/scaling", [ob.name, ob.scale[0], ob.scale[1], ob.scale[2]])

		if ob.type == 'CAMERA':
			camera = bpy.data.cameras[ob.name]
			if not camera.is_updated:
				continue

			perspective = 1
			if camera.type == 'ORTHO':
				perspective = 0
			aspect = scene.game_settings.resolution_y/scene.game_settings.resolution_x
			BLiveClient().send("/data/camera",[ ob.name, camera.angle, aspect, camera.ortho_scale, camera.clip_start, camera.clip_end, perspective, camera.shift_x, camera.shift_y])

		
		#	lamp data except color and energy not working at the moment 
		elif ob.type == 'LAMP':
			'''
				types in BGE SUN, SPOT, NORMAL
			'''
			lamp = bpy.data.lamps[ob.name]
			if not lamp.is_updated:
				continue
			
			#	common data for all lamps types including sun 
			BLiveClient().send("/data/light", [lamp.name, lamp.energy, lamp.color[0], lamp.color[1], lamp.color[2]])
			if lamp.type == 'POINT':
				BLiveClient().send("/data/light/normal", [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation])
			elif lamp.type == 'SPOT':
				BLiveClient().send("/data/light/spot",  [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation, lamp.spot_size, lamp.spot_blend])
			elif lamp.type == 'SUN':
				BLiveClient().send("/data/light/sun", [lamp.name])

	# --- check mesh updates
	for ob in scene.objects:
		if ob.is_updated_data and ob.type == 'MESH':
			try:
				mesh = bmesh.from_edit_mesh(ob.data)
				for face in mesh.faces:
					for vindex, vertex in enumerate(face.verts):
						BLiveClient().send("/data/objects/polygon", [ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2]])
			except ValueError as err:
				print('apphandler.py - mesh update: ', err)

@persistent
def frame_change_post_handler(scene):
	pass
	
@persistent
def load_pre_handler(dummy):
	print("load_post_handler")

@persistent
def save_pre_handler(dummy):
	print("save_pre_handler")

def register():
	print("apphandler.register")
	#~ bpy.app.handlers.frame_change_pre.append(frame_change_post_handler)
	#~ bpy.app.handlers.scene_update_post.append(scene_update_post_handler)
	#~ bpy.app.handlers.load_pre.append(load_pre_handler)
	#~ bpy.app.handlers.save_pre.append(save_pre_handler)

def unregister():
	print("apphandler.unregister")

	#~ idx = bpy.app.handlers.scene_update_post.index(scene_update_post_handler)
	#~ bpy.app.handlers.scene_update_post.remove(bpy.app.handlers.scene_update_post[idx])

	#~ idx = bpy.app.handlers.load_pre.index(load_pre_handler)
	#~ bpy.app.handlers.load_pre.remove(bpy.app.handlers.load_pre[idx])

	#~ idx = bpy.app.handlers.save_pre.index(save_pre_handler)
	#~ bpy.app.handlers.save_pre.remove(bpy.app.handlers.save_pre[idx])
    
