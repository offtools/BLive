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

class BLiveSettings(bpy.types.PropertyGroup):
	"""
		blender wide Settings
	"""
	port = bpy.props.IntProperty(default=9900)
	server = bpy.props.StringProperty(default="127.0.0.1")
	diffuse_to_obcolor = bpy.props.BoolProperty(default=False)
	ztrans_to_obcolor = bpy.props.BoolProperty(default=False)

class BLiveSceneSettings(bpy.types.PropertyGroup):
	"""
		Settings per Scene 
	"""
	server_object = bpy.props.StringProperty()
	has_server_object = bpy.props.BoolProperty(default=False)

def register():
	print("settings.props.register")
	bpy.utils.register_class(BLiveSettings)
	bpy.utils.register_class(BLiveSceneSettings)

	bpy.types.WindowManager.blive_settings = bpy.props.PointerProperty(type=BLiveSettings)
	bpy.types.Scene.blive_scene_settings = bpy.props.PointerProperty(type=BLiveSceneSettings)

	#	initial settings
	#	game engine and GLSL mode
	bpy.context.scene.render.engine = 'BLENDER_GAME'
	bpy.context.scene.game_settings.material_mode = 'GLSL'

def unregister():
	print("settings.props.unregister")
	bpy.utils.unregister_class(BLiveSceneSettings)
	bpy.utils.unregister_class(BLiveSettings)
