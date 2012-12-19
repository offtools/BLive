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
from ..client import BLiveServerSingleton
from ..utils.utils import unique_name

# --- currently harcoded number of channels
dmxpatch = {1,2}
universe = [(i,0) for i in range(512)]
#~ dmxserver = BLiveServer(ip="127.0.0.1", port=20001)

def cb_dmx(path, tags, args, source):
	global universe
	global dmxpatch

	if bpy.context.window_manager.blive_settings.use_olaosc == True:
		data = args[0]

		for channel in dmxpatch:
			value = int(data[channel-1])
			# --- value changed
			if not value == universe[channel-1]:
				universe[channel-1] = int(value)
				if channel == 1 and bool(value>>7):
					if not bpy.context.screen.is_animation_playing is True:
						bpy.ops.screen.animation_play() 
				elif channel == 2:
					bpy.context.active_object.color[3] = float(value/255)

class BLive_OT_olaosc_enable(bpy.types.Operator):
	"""
		Operator - enable olaosc feature
	"""
	bl_idname = "blive.olaosc_enable"
	bl_label = "BLive - enable olaosc "

	def execute(self, context):
		#~ global dmxserver
		context.window_manager.blive_settings.use_olaosc = True
		#~ port = context.window_manager.blive_settings.port+1
		port = 20001
		ip = '127.0.0.1'
		#~ dmxserver.addMsgHandler('/dmx/universe/1', cb_dmx)
		try:
			BLiveServerSingleton(ip, port)
			BLiveServerSingleton().addMsgHandler('/dmx/universe/1', cb_dmx)
		except OSError as err:
			print("#####SIngleton error", err)
		return{'FINISHED'} 

class BLive_OT_olaosc_disable(bpy.types.Operator):
	"""
		Operator - disable olaosc feature
	"""
	bl_idname = "blive.olaosc_disable"
	bl_label = "BLive - disable olaosc "

	def execute(self, context):
		BLiveServerSingleton().close()
		context.window_manager.blive_settings.use_olaosc = False
		return{'FINISHED'} 

#~ class BLive_OT_olaosc_add_channel(bpy.types.Operator):
	#~ """
		#~ Operator - olaosc patch, add channel to patch
	#~ """
	#~ bl_idname = "blive.olaosc_add_channel"
	#~ bl_label = "BLive - olaosc add channel"
	#~ channel = bpy.props.IntProperty(min=1,max=512)
#~ 
	#~ def execute(self, context):
		#~ olaosc = context.scene.olaosc
		#~ universe = olaosc.universes[olaosc.active_universe]
		#~ patch = universe.patch
#~ 
		#~ if not "%s"%self.channel in patch:
			#~ channel = patch.add()
			#~ channel.name = "%s"%self.channel
			#~ return{'FINISHED'}
		#~ else:
			#~ return{'CANCELLED'}
#~ 
#~ class BLive_OT_olaosc_del_channel(bpy.types.Operator):
	#~ """
		#~ Operator - olaosc patch, delete channel
	#~ """
	#~ bl_idname = "blive.olaosc_del_channel"
	#~ bl_label = "BLive - olaosc del channel"
	#~ channel = bpy.props.IntProperty(min=1,max=512)
#~ 
	#~ def execute(self, context):
		#~ olaosc = context.scene.olaosc
		#~ universe = olaosc.universes[olaosc.active_universe]
		#~ patch = universe.patch
#~ 
		#~ if "%s"%self.channel in patch:
			#~ idx = patch.keys().index("%s"%self.channel)
			#~ patch.remove(idx)
			#~ return{'FINISHED'}
		#~ else:
			#~ return{'CANCELLED'}
#~ 
#~ class BLive_OT_olaosc_add_operator(bpy.types.Operator):
	#~ """
		#~ Operator - olaosc add operator to dmx channel
	#~ """
	#~ bl_idname = "blive.olaosc_add_operator"
	#~ bl_label = "BLive - olaosc add operator"
#~ 
	#~ def execute(self, context):
		#~ olaosc = context.scene.olaosc
		#~ universe = olaosc.universes[olaosc.active_universe]
		#~ patch = universe.patch
		#~ channel = patch[universe.active_channel_str]
		#~ op = channel.operator.add()
		#~ op.name = unique_name(channel.operator, "Operator")
		#~ return{'FINISHED'}
#~ 
#~ class BLive_OT_olaosc_del_operator(bpy.types.Operator):
	#~ """
		#~ Operator - olaosc del dmx operator
	#~ """
	#~ bl_idname = "blive.olaosc_del_operator"
	#~ bl_label = "BLive - olaosc del operator"
#~ 
	#~ def execute(self, context):
		#~ olaosc = context.scene.olaosc
		#~ universe = olaosc.universes[olaosc.active_universe]
		#~ patch = universe.patch
		#~ channel = patch[universe.active_channel_str]
		#~ channel.operator.remove(channel.active_operator)
		#~ return{'FINISHED'}

class BLive_OT_olaosc_add_universe(bpy.types.Operator):
	"""
		Operator - add dmx universe
	"""
	bl_idname = "blive.olaosc_add_universe"
	bl_label = "BLive - add dmx universe "

	def execute(self, context):
		olaosc = context.scene.olaosc
		u = olaosc.universes.add()
		u.name = unique_name(olaosc.universes, "Universe")
		u.oscpath = "/universe/dmx/%d"%len(olaosc.universes)
		olaosc.active_by_name = u.name
		
		#TODO: add callback here
		#~ BLiveServerSingleton().addMsgHandler('/dmx/universe/1', cb_dmx)

		return{'FINISHED'}

class BLive_OT_olaosc_del_universe(bpy.types.Operator):
	"""
		Operator - delete dmx universe  
	"""
	bl_idname = "blive.olaosc_del_universe"
	bl_label = "BLive - remove dmx universe "

	def execute(self, context):
		olaosc = context.scene.olaosc
		active = olaosc.active_universe
		olaosc.universes.remove(active)
		return{'FINISHED'}
 
class BLive_OT_olaosc_add_action(bpy.types.Operator):
	"""
		Operator - olaosc create new action
	"""
	bl_idname = "blive.olaosc_add_action"
	bl_label = "BLive - olaosc add action"

	def execute(self, context):
		olaosc = context.scene.olaosc
		universe = olaosc.universes[olaosc.active_universe]
		actions = universe.actions

		action = actions.add()
		action.name = unique_name(actions, "Action")
		return{'FINISHED'}

class BLive_OT_olaosc_del_action(bpy.types.Operator):
	"""
		Operator - olaosc delete action
	"""
	bl_idname = "blive.olaosc_del_action"
	bl_label = "BLive - olaosc delete action"

	def execute(self, context):
		olaosc = context.scene.olaosc
		universe = olaosc.universes[olaosc.active_universe]
		actions = universe.actions

		if len(actions):
			actions.remove(universe.active_action)
			return{'FINISHED'}
		else:
			return{'CANCELLED'}

def register():
	print("olaosc.ops.register")
	bpy.utils.register_class(BLive_OT_olaosc_enable)
	bpy.utils.register_class(BLive_OT_olaosc_disable)
	bpy.utils.register_class(BLive_OT_olaosc_add_universe)
	bpy.utils.register_class(BLive_OT_olaosc_del_universe)
	bpy.utils.register_class(BLive_OT_olaosc_add_action)
	bpy.utils.register_class(BLive_OT_olaosc_del_action)

def unregister():
	print("olaosc.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_olaosc_enable)
	bpy.utils.unregister_class(BLive_OT_olaosc_disable)
	bpy.utils.unregister_class(BLive_OT_olaosc_add_universe)
	bpy.utils.unregister_class(BLive_OT_olaosc_del_universe)
	bpy.utils.unregister_class(BLive_OT_olaosc_add_action)
	bpy.utils.unregister_class(BLive_OT_olaosc_del_action)

