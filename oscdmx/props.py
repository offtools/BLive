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

class BLiveDMXPatch(bpy.types.PropertyGroup):
	"""
		BLive - dmx patch for operators
	"""
	idname = bpy.props.StringProperty()
	prop = bpy.props.StringProperty()
	propidx = bpy.props.IntProperty(default=-1)


class BLiveDMXUniverse(bpy.types.PropertyGroup):
	"""
		BLive - dmx universes
	"""
	universe = bpy.props.StringProperty()
	oscpath = bpy.props.StringProperty()
	patch = bpy.props.PropertyGroup(type=BLiveDMXPatch)
