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
import bmesh
from bpy.app.handlers import persistent
from . import client

@persistent
def scene_update_post_handler(scene):

# tests

	for ob in scene.objects:
		if ob.is_updated:
#			print("object %s updated" %ob)
			pass
		if ob.is_updated_data:
			#print("object updated data %s updated" %ob)
			pass
			
	for ob in bpy.data.materials:
		if ob.is_updated:
			#print("material %s updated" %ob)
			pass
		if ob.is_updated_data:
			#print("material updated data %s updated" %ob)
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
	for ob in scene.objects:
		if ob.type == 'MESH':
			client.client().send("/data/object/color", ob.name, ob.color[0], ob.color[1], ob.color[2], ob.color[3])					

	for ob in scene.objects:
		if ob.is_updated:
			client.client().send("/data/objects", ob.name, ob.location[0], ob.location[1], ob.location[2], ob.rotation_euler[0], ob.rotation_euler[1], ob.rotation_euler[2])

			if ob.type == 'MESH':
				client.client().send("/data/object/scaling", ob.name, ob.scale[0], ob.scale[1], ob.scale[2])					

		if ob.type == 'CAMERA':
			camera = bpy.data.cameras[ob.name]
			if not camera.is_updated:
				continue

			perspective = 1
			if camera.type == 'ORTHO':
				perspective = 0
			aspect = scene.game_settings.resolution_y/scene.game_settings.resolution_x
			client.client().send("/data/camera", ob.name, camera.angle, aspect, camera.ortho_scale, camera.clip_start, camera.clip_end, perspective, camera.shift_x, camera.shift_y)

		
		#	lamp data except color and energy not working at the moment 
		elif ob.type == 'LAMP':
			'''
				types in BGE SUN, SPOT, NORMAL
			'''
			lamp = bpy.data.lamps[ob.name]
			if not lamp.is_updated:
				continue
			
			#	common data for all lamps types including sun 
			client.client().send("/data/light", lamp.name, lamp.energy, lamp.color[0], lamp.color[1], lamp.color[2])
			if lamp.type == 'POINT':
				client.client().send("/data/light/normal", lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation)
			elif lamp.type == 'SPOT':
				client.client().send("/data/light/spot",  lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation, lamp.spot_size, lamp.spot_blend)
			elif lamp.type == 'SUN':
				client.client().send("/data/light/sun", lamp.name)

#	TODO: EDIT MODE											
#if bpy.context.object and bpy.context.object.mode == 'EDIT':
	#	modal operator


	# --- check mesh updates
	for ob in scene.objects:
		if ob.is_updated_data:
			try:
				mesh = bmesh.from_edit_mesh(ob.data)
				for face in mesh.faces:
					for vindex, vertex in enumerate(face.verts):
						client.client().send("/data/objects/polygon", ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2])
			except ValueError as err:
				print('apphandler.py - mesh update: ', err)

@persistent
def frame_change_pre_handler(scene):
	'''
		app handler mainly used to trigger timelinemarkers
	'''
	#   ignored if animation is not playing
	if not bpy.context.screen.is_animation_playing:    
		return

	#   stop animation in editmode
	if not bpy.context.active_object.mode == 'OBJECT':
		if bpy.context.screen.is_animation_playing:
			bpy.ops.screen.animation_play()

	markframes = dict((i.frame, i) for i in scene.timeline_markers)
	cur = scene.frame_current
	prev = cur - 1
	
	#	check for marker in current frame
	if cur in markframes and markframes[cur].name in scene.timeline_queues:
		markerid = markframes[cur].name
		
		if markerid in scene.timeline_queues:
			
			#	check pause - stop animation 
			if scene.timeline_queues[markerid].m_pause and	bpy.context.screen.is_animation_playing:
				bpy.ops.screen.animation_play()
			
			# send events - if not execute_after
			if not scene.timeline_queues[markerid].m_execute_after:
				for item in scene.timeline_queues[markerid].m_items:
					item.trigger()
				
	#	check for marker in prev frame (execute after flag)
	if prev in markframes and markframes[prev].name:
		markerid =  markframes[prev].name
		
		#	check for timelinequeue
		if markerid in scene.timeline_queues:
			
			# send events - execute_after
			if scene.timeline_queues[markerid].m_execute_after:
				for item in scene.timeline_queues[markerid].m_items:
					item.trigger()

@persistent
def frame_change_post_handler(scene):
	pass
	
@persistent
def load_pre_handler(dummy):
	print("load_post_handler")

@persistent
def save_pre_handler(dummy):
	print("save_pre_handler")

#
#	register / unregister functions
#
def register():
	bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler)
	bpy.app.handlers.frame_change_pre.append(frame_change_post_handler)
	bpy.app.handlers.scene_update_post.append(scene_update_post_handler)
	bpy.app.handlers.load_pre.append(load_pre_handler)
	bpy.app.handlers.save_pre.append(save_pre_handler)

def unregister():
	idx = bpy.app.handlers.frame_change_pre.index(frame_change_pre_handler)
	bpy.app.handlers.frame_change_pre.remove(bpy.app.handlers.frame_change_pre[idx])

	idx = bpy.app.handlers.scene_update_post.index(scene_update_post_handler)
	bpy.app.handlers.scene_update_post.remove(bpy.app.handlers.scene_update_post[idx])

	idx = bpy.app.handlers.load_pre.index(load_pre_handler)
	bpy.app.handlers.load_pre.remove(bpy.app.handlers.load_pre[idx])

	idx = bpy.app.handlers.save_pre.index(save_pre_handler)
	bpy.app.handlers.save_pre.remove(bpy.app.handlers.save_pre[idx])
    
