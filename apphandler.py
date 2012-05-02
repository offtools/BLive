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
from bpy.app.handlers import persistent
from . import client

@persistent
def scene_update_post_handler(scene):

	if bpy.data.objects.is_updated:
		for ob in bpy.data.objects:
			if ob.is_updated:
				client.client().send("/data/objects", ob.name, \
													ob.location[0], \
													ob.location[1], \
													ob.location[2], \
													ob.scale[0], \
													ob.scale[1], \
													ob.scale[2], \
													ob.rotation_euler[0], \
													ob.rotation_euler[1], \
													ob.rotation_euler[2], \
													ob.color[0], \
													ob.color[1], \
													ob.color[2], \
													ob.color[3] \
													)

@persistent
def frame_change_pre_handler(scene):
	'''
		app handler used on playback animation
	'''
	#   ignored if animation is not playing
	#   TODO: add BoolProperty in window_manager
	if not bpy.context.screen.is_animation_playing:    
		return

	#   stop animation in editmode
	if not bpy.context.active_object.mode == 'OBJECT':
		if bpy.context.screen.is_animation_playing:
			bpy.ops.screen.animation_play()

	cur = scene.frame_current
	marker = [ (i.frame, i) for i in scene.timeline_markers if i.frame >= cur]
	if len(marker):
		nextmarker = min(marker)[1]
		# animation is passing a marker
		if nextmarker.frame == cur:
			# check if we have an event queue with the same name as the current marker
			if nextmarker.name in bpy.context.scene.timeline_queues:
				# check pause
				if scene.timeline_queues[nextmarker.name].m_pause and bpy.context.screen.is_animation_playing:
					bpy.ops.screen.animation_play()
				# send events
				for item in scene.timeline_queues[nextmarker.name].m_items:
					item.trigger()

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
    
