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

# --- Properties to receive dmx data via OSC (OLA OSC plugin)
# --- remarks:
# --- it should support multiple universes
# --- every scene has its own patch

import bpy

PatchEditMode = (('channels','Channels','List Actions'),
			('actions','Actions','List Channels')
			)

ActionContext = (('ctx_object','Object','Object'),
					('ctx_material','Material','Material'),
					('ctx_texture', 'Texture', 'Texture'),
					('ctx_operator','Operator','Operator')
					)

def update_action(self, context):
	print("update.action")

def update_action_attr(self, context):
	length = 0
	if self.context == 'ctx_object':
		target = context.scene.objects[self.target]
	elif self.context == 'ctx_material':
		target = bpy.data.materials[self.target]
	elif self.context == 'ctx_texture':
		target = bpy.data.textures[self.target]
	elif self.context == 'ctx_operator':
		if not len(self.attr):
			return
		op = eval("bpy.ops.%s"%self.target)
		target = op.get_rna()
	if not self.use_data:
		length = target.bl_rna.properties[self.attr].array_length
		bpy.ops.blive.olaosc_set_attr_arrayidx(length = length)
	else:
		length = target.data.bl_rna.properties[self.attr].array_length
		bpy.ops.blive.olaosc_set_attr_arrayidx(length = length)

class BLiveDMXPatch(bpy.types.PropertyGroup):
	"""
		BLive - DMX Patch
	"""
	action = bpy.props.StringProperty()

class BLiveDMXAction(bpy.types.PropertyGroup):
	"""
		BLive - defines action or data to patch
	"""
	context = bpy.props.EnumProperty(name="context",items=ActionContext)
	target = bpy.props.StringProperty(update=update_action)
	attr = bpy.props.StringProperty(update=update_action_attr)
	min = bpy.props.IntProperty(update=update_action)
	max = bpy.props.IntProperty(update=update_action)
	channel = bpy.props.IntProperty(default=1, min=1, max=255, update=update_action)
	num_channels = bpy.props.IntProperty(default=1, update=update_action)
	use_data = bpy.props.BoolProperty(default=False)
	is_patched = bpy.props.BoolProperty(default=False)

class BLiveDMXUniverse(bpy.types.PropertyGroup):
	"""
		BLive - dmx universes
	"""
	oscpath = bpy.props.StringProperty()
	actions = bpy.props.CollectionProperty(type=BLiveDMXAction)
	patch = bpy.props.CollectionProperty(type=BLiveDMXPatch)
	active_action = bpy.props.IntProperty(default=0)
	active_channel = bpy.props.IntProperty(default=0)
	edit_mode = bpy.props.EnumProperty(name="edit_mode", items=PatchEditMode)

class BLiveDMX(bpy.types.PropertyGroup):
	"""
		BLive - olaosc property wrapper
	"""
	universes = bpy.props.CollectionProperty(type=BLiveDMXUniverse)
	active_universe = bpy.props.IntProperty(default=0)

def register():
	print("olaosc.props.register")
	bpy.utils.register_class(BLiveDMXAction)
	bpy.utils.register_class(BLiveDMXPatch)
	bpy.utils.register_class(BLiveDMXUniverse)
	bpy.utils.register_class(BLiveDMX)

	bpy.types.Scene.olaosc = bpy.props.PointerProperty(type=BLiveDMX)

def unregister():
	print("olaosc.props.unregister")
	bpy.utils.unregister_class(BLiveDMX)
	bpy.utils.unregister_class(BLiveDMXUniverse)
	bpy.utils.register_class(BLiveDMXPatch)
	bpy.utils.register_class(BLiveDMXAction)

	del bpy.types.Scene.olaosc
