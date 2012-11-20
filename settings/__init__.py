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

# Settings holds all common data for the addon. 
# They are added to bpy.data.windowmanger[...], because its
# a unique stucture in the BlendData

from . import props
#~from . import ops
from . import ui

def register():
	print("settings.register")
	props.register()
#~	ops.register()
	ui.register()

def unregister():
	print("settings.unregister")
	ui.unregister()
#~	ops.unregister()
	props.unregister()
