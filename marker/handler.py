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
from . import props
from bpy.app.handlers import persistent

@persistent
def marker_frame_change_pre_handler(scene):
	'''
		app handler mainly used to trigger timelinemarkers
	'''
	#	ignored if animation is not playing
	if not bpy.context.screen.is_animation_playing:    
		return

	#	stop animation in editmode
	if not bpy.context.active_object.mode == 'OBJECT':
		if bpy.context.screen.is_animation_playing:
			bpy.ops.screen.animation_play()
			
	trigger = scene.timeline_trigger
	markerdict = trigger.m_markerdict
	markedframes = dict((i.frame, i) for i in scene.timeline_markers)
	cur = scene.frame_current
	prev = cur - 1
	
	#	check for marker in current frame
	if cur in markedframes and markedframes[cur].name in trigger.m_markerdict:
		markerid = markedframes[cur].name
		
		if markerid in markerdict:
			#	check pause - stop animation
			qid = markerdict[markerid].m_queue
			if trigger.m_queues[qid].m_pause and bpy.context.screen.is_animation_playing:
				bpy.ops.screen.animation_play()
			
			# send events - if not execute_after
			if not trigger.m_queues[qid].m_execute_after:
				for slot in trigger.m_queues[qid].m_slots:
					wrapperitem = getattr(trigger.m_queues[qid].m_trigger, slot.m_type)
					wrapperitem[slot.name].send()

	#	check for marker in prev frame (execute after flag)
	if prev in markedframes and markedframes[prev].name:
		markerid =  markedframes[prev].name
		qid = markerdict[markerid].m_queue
			
		# send events - if execute_after
		if trigger.m_queues[qid].m_execute_after:
			for slot in trigger.m_queues[qid].m_slots:
				wrapperitem = getattr(trigger.m_queues[qid].m_trigger, slot.m_type)
				wrapperitem[slot.name].send()
			
def register():
	print("marker.handler.register")
	bpy.app.handlers.frame_change_pre.append(marker_frame_change_pre_handler)
	
def unregister():
	print("marker.handler.unregister")
	idx = bpy.app.handlers.frame_change_pre.index(marker_frame_change_pre_handler)
	bpy.app.handlers.frame_change_pre.remove(bpy.app.handlers.frame_change_pre[idx])
