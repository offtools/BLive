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
from . import client
from . import properties

##################################################################
#
#    Operators
#
##################################################################

#
#    Operator to add new Timeline Trigger 
#
class BLive_OT_trigger_add(bpy.types.Operator):
	'''
		adds a new trigger to trigger queue and extends TimelineTrigger
		with properties based on requested trigger type
	'''
	bl_idname = "blive.trigger_add"
	bl_label = "BLive add timeline trigger"
	
	type = bpy.props.EnumProperty(items = properties.TRIGGER_TYPE_ENUM, name = "type")

	def execute(self, context):
		if len(context.scene.timeline_markers):
			queue_name = context.scene.timeline_markers[context.scene.active_marker].name

			# query trigger type from TRIGGER_TYPE_ENUM
			trigger_prefix = None
			for i in properties.TRIGGER_TYPE_ENUM:
				if i[0] == self.type:
					trigger_prefix = i[0]
			if not trigger_prefix:
				print('blive.trigger_add - cancelled')
				return{'CANCELLED'}
			
			# add new queue
			if not queue_name in context.scene.timeline_queues:
				queue = bpy.context.scene.timeline_queues.add()
				queue.name = queue_name
			
			# add new trigger entry to queue
			queue = bpy.context.scene.timeline_queues[queue_name]
			item = queue.m_items.add()
			trigger = item.add_trigger(trigger_prefix)
			item.name = trigger.name

		return{'FINISHED'}
		
class BLive_OT_queue_add(bpy.types.Operator):
	'''
	    adds a trigger queue
	'''
	bl_idname = "blive.queue_add"
	bl_label = "BLive add timeline queue"
	
	def execute(self, context):	
		queue_name = context.scene.timeline_markers[context.scene.active_marker].name

		if not queue_name in context.scene.timeline_queues:
			queue = bpy.context.scene.timeline_queues.add()
			queue.name = queue_name
			return{'FINISHED'}
		else:
			return{'CANCELLED'}
			
class BLive_OT_queue_delete(bpy.types.Operator):
	'''
	    deletes a trigger queue
	'''
	bl_idname = "blive.queue_delete"
	bl_label = "BLive delete timeline queue"
	
	def execute(self, context):	
		queue_name = context.scene.timeline_markers[context.scene.active_marker].name

		if queue_name in context.scene.timeline_queues:
			for item in context.scene.timeline_queues[queue_name].m_items:
				item.del_trigger()
			keys = bpy.context.scene.timeline_queues.keys()
			idx = keys.index(queue_name)
			bpy.context.scene.timeline_queues.remove(idx)
			return{'FINISHED'}
		else:
			return{'CANCELLED'}			

class BLive_OT_trigger_delete(bpy.types.Operator):
	'''
		Delete Trigger
	'''
	bl_idname = "blive.trigger_delete"
	bl_label = "BLive delete timeline trigger"
	m_trigger = bpy.props.StringProperty()
	
	def execute(self, context):
		marker = context.scene.active_marker
		idx = context.scene.timeline_queues[marker].m_items.keys().index(self.m_trigger)
		context.scene.timeline_queues[marker].m_items[idx].del_trigger()
		context.scene.timeline_queues[marker].m_items.remove(idx)
		return{'FINISHED'}

class BLive_OT_dummy(bpy.types.Operator):
	'''
		Dummy Operator
	'''
	bl_idname = "blive.dummy"
	bl_label = "BLive Dummy Operator"
	msg = bpy.props.StringProperty(default="")
	
	def execute(self, context):
		print("Dummy Operator: ", self.msg)
		return{'FINISHED'}

#
#    BLive Timeline Marker List located in NLA Editor UI region
#
class BLive_PT_timeline_marker(bpy.types.Panel):
	bl_label = "BLive Timeline Marker"
	bl_space_type = "NLA_EDITOR"
	bl_region_type = "UI"
	
	@classmethod
	def poll(self, context):
		return bool(len(context.scene.timeline_markers))

	def draw(self, context):
		layout = self.layout

		active_marker = context.scene.active_marker
		marker_id = context.scene.timeline_markers[active_marker].name

		#    list of timeline markers 
		scene = context.scene
		row = layout.row()
		row.template_list(scene, "timeline_markers", scene, "active_marker", rows=2, maxrows=2)

		#    add queue
		row = layout.row()
		row.operator("blive.queue_add", text="Add Queue")
		row.operator("blive.queue_delete", text="Del Queue")

		#    boxes for trigger
		if marker_id in context.scene.timeline_queues:
		
			#	queue attr (pause, send after) 
			box = layout.box()
			row = box.row()
			row.prop(context.scene.timeline_queues[marker_id], "m_pause", text="pause")
			row.prop(context.scene.timeline_queues[marker_id], "m_execute_after", text="send after")
					
			#    menu to choose new trigger
			row = layout.row()
			row.operator_menu_enum("blive.trigger_add", "type", text="Add Trigger")

			for item in context.scene.timeline_queues[marker_id].m_items:	
				#    get trigger from queue entry
				trigger = context.scene.timeline_trigger.lookup(item.m_trigger)

				main = layout.column(align=True)
				head = main.box()
				split = head.split(percentage=0.7)
				row = split.row()
				if trigger.m_hidden:
					row.prop(trigger, "m_hidden", text="", icon="TRIA_RIGHT", emboss=False)
				else:
					row.prop(trigger, "m_hidden", text="", icon="TRIA_DOWN", emboss=False)
				row.label( properties.TRIGGER_TYPE_DESCRIPTION(item.m_type) )
				split = split.split(percentage=1)
				buttons = split.column_flow(columns=2, align=True)
				if not trigger.m_applied:
					buttons.prop(trigger, "m_applied", text="", icon="UNLOCKED", toggle=True)
				else:
					buttons.prop(trigger, "m_applied", text="", icon="LOCKED", toggle=True)

				buttons.operator("blive.trigger_delete", text="", icon="PANEL_CLOSE").m_trigger =  item.m_trigger

				if not trigger.m_hidden:
					body = main.box()
					try:
						getattr(self, item.m_type)(context, trigger, body)
					except:
						row = body.row()
						row.label("not implemented")

	def TriggerVideoOpen(self, context, trigger, ui):
		if trigger.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(trigger, "m_filepath", text="Open File", icon="FILE_MOVIE")
		row = ui.row()
		row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
		row = ui.row()
		row.prop_search(trigger, "m_image", bpy.data, "images", text="image")
		row = ui.row()
		row.prop(trigger, "m_loop", text="loop video")

	def TriggerCameraOpen(self, context, trigger, ui):
		if trigger.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(trigger, "m_filepath", text="Open File", icon="FILE_MOVIE")
		row = ui.row()
		row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
		row = ui.row()
		row.prop_search(trigger, "m_image", bpy.data, "images", text="image")
		row = ui.row(align=True)
		row.prop(trigger, "m_width", text="width")
		row.prop(trigger, "m_height", text="height")
		row = ui.row()
		row.prop(trigger, "m_deinterlace", text="deinterlace")

	def TriggerVideoState(self, context, trigger, ui):
		if trigger.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(trigger, "m_state", text="")
		row = ui.row()
		row.prop_search(trigger, "m_image", bpy.data, "images", text="image")

	def TriggerDummy(self, context, trigger, ui):
		if trigger.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(trigger, "m_msg", text="send Message")

def register():
	bpy.utils.register_module(__name__)	

def unregister():
	bpy.utils.unregister_module(__name__)
