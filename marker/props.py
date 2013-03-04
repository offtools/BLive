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

# TODO: user operators instead calling BLiveClient

import bpy
from ..client import BLiveClient

TRIGGER_TYPE_ENUM = [("TriggerDummy","Dummy","Dummy Trigger"), \
			 		("TriggerVideoOpen","Open Video","Open a Video"), \
			 		("TriggerCameraOpen","Connect Camera","Connect a Camera"), \
			 		("TriggerVideoState","Set Video State","Set Play, Pause, Stop"), \
			 		("TriggerChangeScene","Change active Scene","Change active Scene"), \
			 		("TriggerGameProperty","Set a Game Property","Set a Game Property")]
	
def TRIGGER_TYPE_NAME(self, _type):
	types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
	return TRIGGER_TYPE_ENUM[types.index(_type)][1]

def TRIGGER_TYPE_DESCRIPTION(_type):
	types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
	return TRIGGER_TYPE_ENUM[types.index(_type)][2]

class TriggerDummy(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	m_oscpath = bpy.props.StringProperty(default="/debug")

	m_msg = bpy.props.StringProperty(default="Dummy Trigger")

	def send(self):
		BLiveClient().send(self.m_oscpath, [self.m_msg])

class TriggerVideoOpen(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	m_oscpath = bpy.props.StringProperty(default="/texture/movie/open")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()
	m_audio = bpy.props.BoolProperty()
	m_loop = bpy.props.BoolProperty(default=False)
	m_preseek = bpy.props.IntProperty(default=0)
	m_inp = bpy.props.FloatProperty(default=0.0)
	m_outp = bpy.props.FloatProperty(default=0.0)
	m_deinterlace = bpy.props.BoolProperty(default=False)

	def send(self):
		filepath = bpy.path.abspath(self.m_filepath)
		print("send: ", self.m_object, self.m_image, filepath)
		bpy.ops.blive.osc_movie_open(obname=self.m_object,
									imgname=self.m_image,
									filepath=filepath,
									audio=self.m_audio,
									inpoint=self.m_inp,
									outpoint=self.m_outp,
									loop=self.m_loop,
									preseek=self.m_preseek,
									deinterlace=self.m_deinterlace)

class TriggerCameraOpen(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	m_oscpath = bpy.props.StringProperty(default="/texture/camera")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()

	m_width = bpy.props.IntProperty(default=640, min=0)
	m_height = bpy.props.IntProperty(default=480, min=0)
	m_deinterlace = bpy.props.BoolProperty(default=False)
	m_rate = bpy.props.FloatProperty(default=0.0)

	def send(self):
		bpy.ops.blive.osc_camera_open(obname=self.m_object,
										imgname=self.m_image,
										filepath=self.m_filepath,
										width=self.m_width, 
										height=self.m_height, 
										rate=self.m_rate, 
										deinterlace=self.m_deinterlace)

class TriggerVideoState(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	#~ m_oscpath = bpy.props.StringProperty(default="/texture/state")

	m_image = bpy.props.StringProperty()
	m_state = bpy.props.EnumProperty(
	items = [("PLAY","play","play Video"),
			("PAUSE","pause","pause Video"), 
			("STOP","stop","stop Video"),
			("CLOSE","close","reset Texture")],
			name = "state")

	def send(self):
		if self.m_state == "PLAY":
			bpy.ops.blive.osc_videotexture_play(imgname=self.m_image)
		elif self.m_state == "PAUSE":
			bpy.ops.blive.osc_videotexture_pause(imgname=self.m_image)
		elif self.m_state == "STOP":
			bpy.ops.blive.osc_videotexture_stop(imgname=self.m_image)
		elif self.m_state == "CLOSE":
			bpy.ops.blive.osc_videotexture_close(imgname=self.m_image)

class TriggerChangeScene(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	m_oscpath = bpy.props.StringProperty(default="/scene/active")
	m_scene = bpy.props.StringProperty()

	def send(self):
		#	change scene in blender too
		bpy.context.screen.scene = bpy.data.scenes[self.m_scene]
		BLiveClient().send(self.m_oscpath, [self.m_scene])

class TriggerGameProperty(bpy.types.PropertyGroup):
	m_hidden = bpy.props.BoolProperty(default=True)
	m_oscpath = bpy.props.StringProperty(default="/data/object/gameproperty")

	m_object = bpy.props.StringProperty()
	m_property = bpy.props.StringProperty()

	def send(self):
		value = bpy.context.scene.objects[self.m_object].game.properties[self.m_property].value
		BLiveClient().send(self.m_oscpath, [self.m_object, self.m_property, value])

class TriggerWrapper(bpy.types.PropertyGroup):
	'''
		Property Group for OscTrigger
	'''
	TriggerDummy = bpy.props.CollectionProperty(type=TriggerDummy)
	TriggerVideoOpen = bpy.props.CollectionProperty(type=TriggerVideoOpen)
	TriggerCameraOpen = bpy.props.CollectionProperty(type=TriggerCameraOpen)
	TriggerVideoState = bpy.props.CollectionProperty(type=TriggerVideoState)
	TriggerChangeScene = bpy.props.CollectionProperty(type=TriggerChangeScene)
	TriggerGameProperty = bpy.props.CollectionProperty(type=TriggerGameProperty)

class TriggerSlot(bpy.types.PropertyGroup):
	m_type = bpy.props.StringProperty()
	m_hidden = bpy.props.BoolProperty(default=True)

class TriggerQueue(bpy.types.PropertyGroup):
	m_execute_after = bpy.props.BoolProperty(default=False)
	m_pause = bpy.props.BoolProperty(default=True)
	m_trigger = bpy.props.PointerProperty(type=TriggerWrapper)	
	m_slots = bpy.props.CollectionProperty(type=TriggerSlot)
	m_sel_slot = bpy.props.StringProperty()

class MarkerDict(bpy.types.PropertyGroup):
	m_queue = bpy.props.StringProperty()
	
class TimelineTrigger(bpy.types.PropertyGroup):
	m_markerdict = bpy.props.CollectionProperty(type=MarkerDict)
	m_queues = bpy.props.CollectionProperty(type=TriggerQueue)
	m_sel_marker = bpy.props.IntProperty(default = 0)
	
def register():
	print("marker.props.register")
	
	bpy.utils.register_class(TriggerDummy)
	bpy.utils.register_class(TriggerVideoOpen)
	bpy.utils.register_class(TriggerCameraOpen) 
	bpy.utils.register_class(TriggerVideoState)
	bpy.utils.register_class(TriggerChangeScene)
	bpy.utils.register_class(TriggerGameProperty)
	bpy.utils.register_class(TriggerWrapper)
	bpy.utils.register_class(TriggerSlot)
	bpy.utils.register_class(TriggerQueue)
	bpy.utils.register_class(MarkerDict)
	bpy.utils.register_class(TimelineTrigger)
		
	bpy.types.Scene.timeline_trigger = bpy.props.PointerProperty(type=TimelineTrigger, options={"HIDDEN"})
	
def unregister():
	print("marker.props.unregister")

	del bpy.types.Scene.timeline_trigger

	bpy.utils.unregister_class(TriggerDummy)
	bpy.utils.unregister_class(TriggerVideoOpen)
	bpy.utils.unregister_class(TriggerCameraOpen) 
	bpy.utils.unregister_class(TriggerVideoState)
	bpy.utils.unregister_class(TriggerChangeScene)
	bpy.utils.unregister_class(TriggerGameProperty)
	bpy.utils.unregister_class(TriggerQueue)
	bpy.utils.unregister_class(TriggerSlot)
	bpy.utils.unregister_class(TriggerWrapper)
	bpy.utils.unregister_class(MarkerDict)
	bpy.utils.unregister_class(TimelineTrigger)
