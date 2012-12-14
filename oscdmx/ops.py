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

# --- currently harcoded number of channels
dmxpatch = {1,2}
universe = [(i,0) for i in range(512)]
#~ dmxserver = BLiveServer(ip="127.0.0.1", port=20001)

def cb_dmx(path, tags, args, source):
	global universe
	global dmxpatch

	if bpy.context.window_manager.blive_settings.use_dmx_over_osc == True:
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

class BLive_OT_oscdmx_enable(bpy.types.Operator):
	"""
		Operator - enable oscdmx feature
	"""
	bl_idname = "blive.oscdmx_enable"
	bl_label = "BLive - enable oscdmx "

	def execute(self, context):
		#~ global dmxserver
		context.window_manager.blive_settings.use_dmx_over_osc = True
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

class BLive_OT_oscdmx_disable(bpy.types.Operator):
	"""
		Operator - disable oscdmx feature
	"""
	bl_idname = "blive.oscdmx_disable"
	bl_label = "BLive - disable oscdmx "

	def execute(self, context):
		#~ global dmxserver
		#~ dmxserver.close()
		BLiveServerSingleton().close()
		context.window_manager.blive_settings.use_dmx_over_osc = False
		return{'FINISHED'} 

class BLive_OT_oscdmx_patch(bpy.types.Operator):
	"""
		Operator - patch oscdmx
	"""
	bl_idname = "blive.oscdmx_patch"
	bl_label = "BLive - patch oscdmx "

	def execute(self, context):
		global patch
		from . import patch
		lpatch = patch.test
		return{'FINISHED'} 

def register():
	print("oscdmx.ops.register")
	bpy.utils.register_class(BLive_OT_oscdmx_enable)
	bpy.utils.register_class(BLive_OT_oscdmx_disable)
	bpy.utils.register_class(BLive_OT_oscdmx_patch)

def unregister():
	print("oscdmx.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_oscdmx_enable)
	bpy.utils.unregister_class(BLive_OT_oscdmx_disable)
	bpy.utils.unregister_class(BLive_OT_oscdmx_patch)
