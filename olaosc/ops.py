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
from ..client import BLiveServer
from ..utils.utils import unique_name

class OLAOSCServer(BLiveServer):
	def __init__(self, ip="127.0.0.1", port=9900):
		super().__init__(ip, port)

server = None

def ServerInstance():
	global server
	return server

def cb_dmx(path, tags, args, source):
	if bpy.context.window_manager.blive_settings.use_olaosc == True:
		data = args[0]
		olaosc = bpy.context.scene.olaosc
		universe = olaosc.universes[olaosc.active_universe]
		patch = universe.patch

		for key in patch.keys():
			value = data[int(key)-1]
			id_action = patch[key].action
			action = universe.actions[id_action]

			# --- Objects
			if action.context == "ctx_object":
				target = bpy.context.scene.objects[action.target]
				if action.use_data:
					target = target.data
				if hasattr(action, "attr_idx"):
					prop = getattr(target, action.attr)
					prop[int(action.attr_idx)] = value/255
					print(prop, value/255)
				else:
					setattr(target, action.attr, value/255)

			if action.context == "ctx_material":
				bpy.data.materials[action.target]

			if action.context == "ctx_texture":
				bpy.data.textures[action.target]

			if action.context == "ctx_operator":
				op = eval("bpy.ops.%s"%action.target)
				target = op.get_rna()

class BLive_OT_olaosc_enable(bpy.types.Operator):
	"""
		Operator - enable olaosc feature
	"""
	bl_idname = "blive.olaosc_enable"
	bl_label = "BLive - enable olaosc "

	def execute(self, context):
		global server
		context.window_manager.blive_settings.use_olaosc = True
		port = context.window_manager.blive_settings.olaosc_port
		ip = context.window_manager.blive_settings.olaosc_server
		try:
			server = OLAOSCServer(ip, port)
			print(server)
		except OSError as err:
			print("OLA OSC: ", err)
		return{'FINISHED'} 

class BLive_OT_olaosc_disable(bpy.types.Operator):
	"""
		Operator - disable olaosc feature
	"""
	bl_idname = "blive.olaosc_disable"
	bl_label = "BLive - disable olaosc "

	def execute(self, context):
		global server
		if server:
			server.close()
			server = None
			context.window_manager.blive_settings.use_olaosc = False
		return{'FINISHED'} 

class BLive_OT_olaosc_set_attr_arrayidx(bpy.types.Operator):
	"""
		Operator - set array idx enum
	"""
	bl_idname = "blive.olaosc_set_attr_arrayidx"
	bl_label = "BLive - set attr arrayidx"
	length = bpy.props.IntProperty()

	def execute(self, context):
		if self.length:
			gen = [ (str(i),str(i),'') for i in range(self.length) ]
			bpy.types.BLiveDMXAction.attr_idx = bpy.props.EnumProperty(name="attr_idx", items=gen)
		return{'FINISHED'}

class BLive_OT_olaosc_add_universe(bpy.types.Operator):
	"""
		Operator - add dmx universe
	"""
	bl_idname = "blive.olaosc_add_universe"
	bl_label = "BLive - add dmx universe "

	def execute(self, context):
		global server
		olaosc = context.scene.olaosc
		u = olaosc.universes.add()
		u.name = unique_name(olaosc.universes, "Universe")
		u.oscpath = "/dmx/universe/%d"%len(olaosc.universes)
		olaosc.active_by_name = u.name
		
		if ServerInstance():
			print(u.oscpath)
			ServerInstance().addMsgHandler(u.oscpath, cb_dmx)

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

class BLive_OT_olaosc_patch(bpy.types.Operator):
	"""
		Operator - olaosc patch channel
	"""
	bl_idname = "blive.olaosc_patch"
	bl_label = "BLive - olaosc patch channel"

	def execute(self, context):
		olaosc = context.scene.olaosc
		universe = olaosc.universes[olaosc.active_universe]
		action = universe.actions[universe.active_action]
		req_chan = action.channel
		num_chan = action.num_channels

		# --- check if channels already set
		for i in range(num_chan):
			chan = req_chan + i
			if "%s"%chan in universe.patch:
				action.is_patched = False
				return{'CANCELLED'}

		for i in range(num_chan):
			chan = universe.patch.add()
			chan.name = "%s"%(req_chan + i)
			chan.action = action.name
			action.is_patched = True
		return{'FINISHED'}

class BLive_OT_olaosc_unpatch(bpy.types.Operator):
	"""
		Operator - olaosc unpatch channel
	"""
	bl_idname = "blive.olaosc_unpatch"
	bl_label = "BLive - olaosc unpatch channel"

	def execute(self, context):
		olaosc = context.scene.olaosc
		universe = olaosc.universes[olaosc.active_universe]
		action = universe.actions[universe.active_action]
		req_chan = action.channel
		num_chan = action.num_channels

		for i in range(num_chan):
			chan = req_chan + 1
			if "%s"%chan in universe.patch:
				universe.patch.remove(universe.patch.keys().index("%s"%chan))
				action.is_patched = False
				return{'CANCELLED'}

def register():
	print("olaosc.ops.register")
	bpy.utils.register_class(BLive_OT_olaosc_enable)
	bpy.utils.register_class(BLive_OT_olaosc_disable)
	bpy.utils.register_class(BLive_OT_olaosc_set_attr_arrayidx)
	bpy.utils.register_class(BLive_OT_olaosc_add_universe)
	bpy.utils.register_class(BLive_OT_olaosc_del_universe)
	bpy.utils.register_class(BLive_OT_olaosc_add_action)
	bpy.utils.register_class(BLive_OT_olaosc_del_action)
	bpy.utils.register_class(BLive_OT_olaosc_patch)
	bpy.utils.register_class(BLive_OT_olaosc_unpatch)

def unregister():
	print("olaosc.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_olaosc_enable)
	bpy.utils.unregister_class(BLive_OT_olaosc_disable)
	bpy.utils.unregister_class(BLive_OT_olaosc_set_attr_arrayidx)
	bpy.utils.unregister_class(BLive_OT_olaosc_add_universe)
	bpy.utils.unregister_class(BLive_OT_olaosc_del_universe)
	bpy.utils.unregister_class(BLive_OT_olaosc_add_action)
	bpy.utils.unregister_class(BLive_OT_olaosc_del_action)
	bpy.utils.unregister_class(BLive_OT_olaosc_patch)
	bpy.utils.unregister_class(BLive_OT_olaosc_unpatch)

