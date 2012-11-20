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

#	TODO: map diffuse color of material slot[0] to Object Color
#	TODO: map Z-Transparency | Ray | ... of material slot[0] to Object Color[4]
#	(reuse Keyframe when rendering your Project instead of using gameengine)

#	FIXME: change Scene Trigger

class CameraExtProperties():
	#	Menu Projektor
	#row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
	def register():
		#	extra Camera Properties
		bpy.types.Camera.lens_max = bpy.props.FloatProperty(update=CameraExtProperties.callback)
		bpy.types.Camera.lens_min = bpy.props.FloatProperty(update=CameraExtProperties.callback)
		bpy.types.Camera.hlens_min = bpy.props.FloatProperty(update=CameraExtProperties.callback)
		bpy.types.Camera.hlens_max = bpy.props.FloatProperty(update=CameraExtProperties.callback)
		bpy.types.Camera.vlens_min = bpy.props.FloatProperty(update=CameraExtProperties.callback)
		bpy.types.Camera.vlens_max = bpy.props.FloatProperty(update=CameraExtProperties.callback)	

	def unregister():
		del bpy.types.Camera.lens_max
		del bpy.types.Camera.lens_min
		del bpy.types.Camera.hlens_min
		del bpy.types.Camera.hlens_max
		del bpy.types.Camera.vlens_min
		del bpy.types.Camera.vlens_max
		
	def callback():
		pass

