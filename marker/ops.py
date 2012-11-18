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
from .props import TRIGGER_TYPE_ENUM
from .props import TRIGGER_TYPE_DESCRIPTION

def unique_name(collection, name):
	'''
		find a unique name for a new object in a collection
	'''
	def check_name(collection, name, num):
	
		if "{0}.{1}".format(name, str(num).zfill(3)) in collection:
			return check_name(collection, name, num+1)
		return num
	
	if not name in collection:
		return name

	num = check_name(collection, name, 1)
	unique = "{0}.{1}".format(name, str(num).zfill(3))
	return unique

class BLive_OT_trigger_new(bpy.types.Operator):
	'''
		add timeline trigger
	'''
	bl_idname = "blive.trigger_new"
	bl_label = "BLive add a timeline trigger"

	def execute(self, context):
		trigger = context.scene.timeline_trigger
		marker = context.scene.timeline_markers[trigger.m_sel_marker]
		item = trigger.m_queues.add()
		item.name = unique_name(trigger.m_queues, marker.name)
		if not marker.name in trigger.m_markerdict:
			entry = trigger.m_markerdict.add()
			entry.name = marker.name
		trigger.m_markerdict[marker.name].m_queue = item.name
		return{'FINISHED'}

class BLive_OT_trigger_delete(bpy.types.Operator):
	'''
		delete timeline trigger
	'''
	bl_idname = "blive.trigger_delete"
	bl_label = "BLive delete a timeline trigger"

	def execute(self, context):
		trigger = context.scene.timeline_trigger
		marker = context.scene.timeline_markers[trigger.m_sel_marker]
		if not marker.name in trigger.m_markerdict:
			return{'CANCELED'}
		qid = trigger.m_markerdict[marker.name].m_queue
		#	remove queue
		if qid in trigger.m_queues:
			queue = trigger.m_queues[qid]
			idx = trigger.m_queues.keys().index(qid)
			trigger.m_queues.remove(idx)
			#	remove markerdict entry
			idx = trigger.m_markerdict.keys().index(marker.name)
			trigger.m_markerdict.remove(idx)			
			return{'FINISHED'}
		else:
			return{'CANCELED'}

#~ class BLive_OT_trigger_assign(bpy.types.Operator):
	#~ '''
		#~ assign trigger to timeline marker
	#~ '''
	#~ bl_idname = "blive.trigger_assign"
	#~ bl_label = "BLive assign a trigger to a timeline marker"
	#~ qid = bpy.props.StringProperty()
#~ 
	#~ def execute(self, context):
		#~ trigger = conext.scene.timeline_trigger
		#~ if not len(qid) or not qid in trigger.m_queues:
			#~ return{'CANCELED'}
		#~ marker = conext.scene.timeline_markers[trigger.m_sel_marker]
		#~ if not marker.name in trigger.m_markerdict:
			#~ entry = trigger.m_markerdict.add()
			#~ entry.name = marker.name
		#~ trigger.m_markerdict[marker.name].m_queue = qid
		#~ return{'FINISHED'}
	
class BLive_OT_trigger_revoke(bpy.types.Operator):
	'''
		revoke trigger from timeline marker
	'''
	bl_idname = "blive.trigger_revoke"
	bl_label = "BLive revoke a trigger from a timeline marker"
	
	def execute(self, context):
		trigger = context.scene.timeline_trigger
		marker = context.scene.timeline_markers[trigger.m_sel_marker]
		if marker.name in trigger.m_markerdict:
			idx = trigger.m_markerdict.keys().index(marker.name)
			trigger.m_markerdict.remove(idx)				
		return{'FINISHED'}

class BLive_OT_trigger_append(bpy.types.Operator):
	'''
		appends a new trigger item to trigger queue
	'''
	bl_idname = "blive.trigger_append"
	bl_label = "BLive add items to timeline trigger"
	type = bpy.props.EnumProperty(items = TRIGGER_TYPE_ENUM, name = "type")

	def execute(self, context):
		#	TODO: implement blive.trigger_append operator
		trigger = context.scene.timeline_trigger
		marker = context.scene.timeline_markers[trigger.m_sel_marker]
		if not marker.name in trigger.m_markerdict:
			print("error append - no markername in markerdict")
			return{'CANCELED'}
		qid = trigger.m_markerdict[marker.name].m_queue
		if qid in trigger.m_queues:
			queue = trigger.m_queues[qid]
			slot = queue.m_slots.add()
			slot.name = unique_name(queue.m_slots, self.type)
			slot.m_type = self.type
			wrapperentry = getattr(queue.m_trigger, self.type)
			entry = wrapperentry.add()
			entry.name = slot.name
			return{'FINISHED'}
		else:
			print('error in append - no qid in m_queues')
			return{'CANCELED'}	
		return{'FINISHED'}
		
class BLive_OT_trigger_remove(bpy.types.Operator):
	'''
		removes trigger item from trigger queue
	'''
	bl_idname = "blive.trigger_remove"
	bl_label = "BLive remove item from timeline trigger queue"
	m_slot = bpy.props.StringProperty()
	
	def execute(self, context):
		trigger = context.scene.timeline_trigger
		marker = context.scene.timeline_markers[trigger.m_sel_marker]
		qid = trigger.m_markerdict[marker.name].m_queue
		queue = trigger.m_queues[qid]

		if self.m_slot in queue.m_slots:
			print("blive.trigger_remove", self.m_slot, queue.m_slots[self.m_slot].m_type)
			wrapperentry = getattr(queue.m_trigger, queue.m_slots[self.m_slot].m_type)
			idx = queue.m_slots.keys().index(self.m_slot)
			queue.m_slots.remove(idx)
			idx = wrapperentry.keys().index(self.m_slot)
			wrapperentry.remove(idx)
		return{'FINISHED'}
				
def register():
	print("marker.ops.register")
	bpy.utils.register_class(BLive_OT_trigger_new)
	bpy.utils.register_class(BLive_OT_trigger_delete)
	#~ bpy.utils.register_class(BLive_OT_trigger_assign)
	bpy.utils.register_class(BLive_OT_trigger_revoke)
	bpy.utils.register_class(BLive_OT_trigger_append)
	bpy.utils.register_class(BLive_OT_trigger_remove)

def unregister():
	print("marker.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_trigger_new)
	bpy.utils.unregister_class(BLive_OT_trigger_delete)
	#~ bpy.utils.unregister_class(BLive_OT_trigger_assign)
	bpy.utils.unregister_class(BLive_OT_trigger_revoke)
	bpy.utils.unregister_class(BLive_OT_trigger_append)
	bpy.utils.unregister_class(BLive_OT_trigger_remove)
