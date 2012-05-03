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

#	TODO: move all methods, which manipulate the properties into operators

##################################################################
#
#    Property Defs for Timeline Trigger
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
		print("connect camera")
		client.client().send(self.m_oscpath, self.m_object, self.m_image, self.m_filepath)

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

class TimelineQueue(bpy.types.PropertyGroup):
	'''
		PropertyGroup of Trigger Queues, stores Entries with Trigger
	'''
	m_items = bpy.props.CollectionProperty(type=TimelineQueueEntry)
	m_execute_after = bpy.props.BoolProperty(default=False)
	m_pause = bpy.props.BoolProperty(default=True)


def register():

	##################################################################
	#
	#    register
	#
	##################################################################

	bpy.utils.register_class(TimelineTriggerDummy)
	bpy.utils.register_class(TimelineTriggerVideoOpen)
	bpy.utils.register_class(TimelineTriggerCameraOpen)	
	bpy.utils.register_class(TimelineTriggerVideoState)
	bpy.utils.register_class(TimelineTrigger)
	bpy.utils.register_class(TimelineQueueEntry)
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
	
def unregister():

	##################################################################
	#
	#    unregister
	#
	##################################################################

	bpy.utils.unregister_class(TimelineTriggerDummy)
	bpy.utils.unregister_class(TimelineTriggerVideoOpen)
	bpy.utils.unregister_class(TimelineTriggerCameraOpen)	
	bpy.utils.unregister_class(TimelineTriggerVideoState)
	bpy.utils.unregister_class(TimelineTrigger)
	bpy.utils.unregister_class(TimelineQueueEntry)
	bpy.utils.unregister_class(TimelineQueue)
	
	##################################################################
	#
	#    cleanup
	#
	##################################################################

	del bpy.types.Scene.timeline_trigger
	del bpy.types.Scene.timeline_queues
	del bpy.types.Scene.active_marker
