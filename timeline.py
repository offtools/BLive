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

##################################################################
#
#    Type Defs for Timeline Trigger
#
##################################################################

TRIGGER_TYPE_ENUM = [("TriggerDummy","Dummy","Dummy Trigger"), \
			 		("TriggerVideoOpen","Open Video","Open a Video"), \
			 		("TriggerCameraOpen","Connect Camera","Connect a Camera"), \
			 		("TriggerVideoState","Set Video State","Set Play, Pause, Stop")]

def TRIGGER_TYPE_NAME(self, _type):
	types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
	return TRIGGER_TYPE_ENUM[types.index(_type)][1]

def TRIGGER_TYPE_DESCRIPTION(_type):
	types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
	return TRIGGER_TYPE_ENUM[types.index(_type)][2]

class TimelineTriggerDummy(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# trigger type definded in TRIGGER_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # trigger is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # trigger is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/debug")

	m_msg = bpy.props.StringProperty(default="Dummy Trigger")

	def send(self):
		client.client().send(self.m_oscpath, self.m_msg)

bpy.utils.register_class(TimelineTriggerDummy)

class TimelineTriggerVideoOpen(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# trigger type definded in TRIGGER_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # trigger is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # trigger is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/movie")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()

	def send(self):
		print("play movie")
		filepath = bpy.path.abspath(self.m_filepath)
		client.client().send(self.m_oscpath, self.m_object, self.m_image, filepath)

bpy.utils.register_class(TimelineTriggerVideoOpen)

class TimelineTriggerCameraOpen(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# trigger type definded in TRIGGER_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # trigger is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # trigger is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/camera")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()

	def send(self):
#		filepath = bpy.path.abspath(self.m_filepath)
		print("connect camera")
		client.client().send(self.m_oscpath, self.m_object, self.m_image, self.m_filepath)

bpy.utils.register_class(TimelineTriggerCameraOpen)

class TimelineTriggerVideoState(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# trigger type definded in TRIGGER_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # trigger is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # trigger is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/state")

	m_image = bpy.props.StringProperty()
	m_state = bpy.props.EnumProperty(
		items = [("PLAY","play","play Video"),
				("PAUSE","pause","pause Video"), 
				("STOP","stop","stop Video"),
				("REMOVE","remove","remove dynamic Texture")],
		name = "state")

	def send(self):
		client.client().send(self.m_oscpath, self.m_image, self.m_state)
		
bpy.utils.register_class(TimelineTriggerVideoState)

class TimelineTrigger(bpy.types.PropertyGroup):
	'''
		Property Group that holds all Trigger, sorted by types
	'''
	
	#TODO: use keys instead of TRIGGER_TYPE_ENUM

	TriggerDummy = bpy.props.CollectionProperty(type=TimelineTriggerDummy)
	TriggerVideoOpen = bpy.props.CollectionProperty(type=TimelineTriggerVideoOpen)
	TriggerCameraOpen = bpy.props.CollectionProperty(type=TimelineTriggerCameraOpen)
	TriggerVideoState = bpy.props.CollectionProperty(type=TimelineTriggerVideoState)
	
	m_types = bpy.props.EnumProperty(items = TRIGGER_TYPE_ENUM, name = "state")


	def add(self, _type):
		'''
			add a new trigger to the Triggercollections
		'''
		for info in TRIGGER_TYPE_ENUM:
			if _type == info[0]:
				entry = getattr(self, info[0]).add()
				entry.m_type = info[0]
				entry.m_hidden = False
				entry.m_applied = False
				
				# search for a unique name
				def check_name(collection, name, num):
					if "{0}.{1}".format(name, str(num).zfill(3)) in collection:
						return check_name(collection, name, num+1)
					return num

				num = check_name(getattr(self, info[0]), info[0], 1)
				entry.name = "{0}.{1}".format(info[0], str(num).zfill(3))
				print("test add: ", entry.name)

				return entry

	def remove(self, name):
		'''
			removes an trigger ()
		'''
		print("TimelineTrigger.remove: ", name)
		def get_type(name):
			for i in TRIGGER_TYPE_ENUM:
				if i[0] == name[:-4]:
					return i[0]

		_type = get_type(name)

		if not _type in self.keys():
			raise TypeError("requested type not found in timeline trigger")

		collection = getattr(self, _type)

		if not name in collection:
			raise IndexError("requested trigger name not found in timeline trigger")

		idx = collection.keys().index(name)
		collection.remove(idx)			

	def lookup(self, _name):
		def get_type(_name):
			for i in TRIGGER_TYPE_ENUM:
				if i[0] == _name[:-4]:
					return i[0]

		_type = get_type(_name)

		if not _type in self.keys():
			raise TypeError("requested type not found in timeline trigger")

		collection = getattr(self, _type)

		if not _name in collection:
			raise IndexError("requested trigger name not found in timeline trigger")

		return collection[_name]

bpy.utils.register_class(TimelineTrigger)

class TimelineQueueEntry(bpy.types.PropertyGroup):
	'''
		PropertyGroup for Trigger Queue Entries, references diff type of Trigger
	'''
	m_marker = bpy.props.StringProperty()	# name of the queue id
	m_type = bpy.props.StringProperty()		# trigger type	
	m_trigger = bpy.props.StringProperty() 	# trigger name

	def add_trigger(self, triggertype):
		'''
			add a new trigger
		'''
		trigger = bpy.context.scene.timeline_trigger.add(triggertype)
		self.m_trigger = trigger.name
		self.m_type = trigger.m_type
		return trigger

	def del_trigger(self):
		'''
			delete referenced trigger
		'''
		print("TimelineQueueEntry.del_trigger: ", self.m_marker, self.m_type, self.m_trigger)
		bpy.context.scene.timeline_trigger.remove(self.m_trigger)

	def trigger(self):
		bpy.context.scene.timeline_trigger.lookup(self.m_trigger).send()

bpy.utils.register_class(TimelineQueueEntry)

class TimelineQueue(bpy.types.PropertyGroup):
	'''
		PropertyGroup of Trigger Queues, stores Entries with Trigger
	'''
	m_items = bpy.props.CollectionProperty(type=TimelineQueueEntry)
	m_execute_after = bpy.props.BoolProperty(default=False)
	m_pause = bpy.props.BoolProperty(default=True)

bpy.utils.register_class(TimelineQueue)


##################################################################
#
#    init Instances
#
##################################################################

#	Instanciate on register and remove on unregister
bpy.types.Scene.timeline_trigger = bpy.props.PointerProperty(type=TimelineTrigger, options={"HIDDEN"})
bpy.types.Scene.timeline_queues = bpy.props.CollectionProperty(type=TimelineQueue, options={"HIDDEN"})

#	TODO: change to dynamic Property (no need to store in blendfile)
bpy.types.Scene.active_marker = bpy.props.IntProperty(options={"HIDDEN"}, subtype='UNSIGNED')

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
	
	type = bpy.props.EnumProperty(items = TRIGGER_TYPE_ENUM, name = "type")

	def execute(self, context):
		if len(context.scene.timeline_markers):
			queue_name = context.scene.timeline_markers[context.scene.active_marker].name

			# query trigger type from TRIGGER_TYPE_ENUM
			trigger_prefix = None
			for i in TRIGGER_TYPE_ENUM:
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
				row.label( TRIGGER_TYPE_DESCRIPTION(item.m_type) )
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

	def TriggerCameraOpen(self, context, trigger, ui):
		if trigger.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(trigger, "m_filepath", text="Open File", icon="FILE_MOVIE")
		row = ui.row()
		row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
		row = ui.row()
		row.prop_search(trigger, "m_image", bpy.data, "images", text="image")
		
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
		
def unregister():
	bpy.utils.unregister_module(__name__)
