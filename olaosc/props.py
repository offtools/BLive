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

class BLiveDMXOperator(bpy.types.PropertyGroup):
	"""
		BLive - dmx patch for operators
	"""
	op = bpy.props.StringProperty()
	param = bpy.props.StringProperty()
	paramidx = bpy.props.IntProperty(default=-1)

class BLiveDMXChannel(bpy.types.PropertyGroup):
	"""
		BLive - dmx channel
	"""
	active_operator = bpy.props.IntProperty(default=-1)
	operator = bpy.props.CollectionProperty(type=BLiveDMXOperator)

PatchContext = (('ctx_object','Object','Object'),
					('ctx_material','Material','Material'),
					('ctx_texture', 'Texture', 'Texture'),
					('ctx_operator','Operator','Operator')
					)

class BLiveDMXActionPatch(bpy.types.PropertyGroup):
	"""
		BLive - defines action or data to patch
	"""
	context = bpy.props.StringProperty()
	target = bpy.props.StringProperty()
	attr = bpy.props.StringProperty()
	attr_idx = bpy.props.IntProperty(default=0, min=0, max=4)
	precision = bpy.props.IntProperty(default=2, min=0, max=4)
	min = bpy.props.IntProperty()
	max = bpy.props.IntProperty()
	channel = bpy.props.IntProperty()
	num_channels = bpy.props.IntProperty()

class BLiveDMXUniverse(bpy.types.PropertyGroup):
	"""
		BLive - dmx universes
	"""
	oscpath = bpy.props.StringProperty()
	actions = bpy.props.CollectionProperty(type=BLiveDMXActionPatch)
	active_action = bpy.props.IntProperty(default=0)
	context = bpy.props.EnumProperty(name="context",items=PatchContext)

class BLiveDMX(bpy.types.PropertyGroup):
	"""
		BLive - olaosc property wrapper
	"""
	universes = bpy.props.CollectionProperty(type=BLiveDMXUniverse)
	active_universe = bpy.props.IntProperty(default=0)

def register():
	print("olaosc.props.register")
	bpy.utils.register_class(BLiveDMXOperator)
	bpy.utils.register_class(BLiveDMXChannel)
	bpy.utils.register_class(BLiveDMXActionPatch)
	bpy.utils.register_class(BLiveDMXUniverse)
	bpy.utils.register_class(BLiveDMX)

	bpy.types.Scene.olaosc = bpy.props.PointerProperty(type=BLiveDMX)

def unregister():
	print("olaosc.props.unregister")
	bpy.utils.unregister_class(BLiveDMX)
	bpy.utils.unregister_class(BLiveDMXUniverse)
	bpy.utils.register_class(BLiveDMXActionPatch)
	bpy.utils.unregister_class(BLiveDMXChannel)
	bpy.utils.unregister_class(BLiveDMXOperator)

	del bpy.types.Scene.olaosc
