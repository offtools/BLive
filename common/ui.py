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

# FIXME: max. Port number in game property is 10000

import bpy

###############################################
#
#	Blive Scene Settings Panel
#
###############################################

class BLive_PT_common_settings(bpy.types.Panel):
	bl_label = "BLive Settings"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"

	def draw(self, context):
		layout = self.layout
		bs = context.window_manager.blive_settings
		
		row = layout.row()
		row.label("Blive Server Settings")
		row = layout.row(align=True)
		row.prop(bs, "server", text="Server")
		row.prop(bs, "port", text="")

		layout. separator()
		
		row = layout.row()
		row.label("Material Hacks")
		row = layout.row()
		row.prop(bs, "diffuse_to_obcolor", text="Diffuse and Transparency to ObColor")

###############################################
#
#	Blive Scene Settings Panel
#
###############################################

class BLive_PT_scene_settings(bpy.types.Panel):
	bl_label = "BLive Scene Settings"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def draw(self, context):
		
		sc = context.scene
		bs = sc.blive_scene_settings
		layout = self.layout
		
		row = layout.row()
		row.label("choose object for server gamelogic:")
		search = layout.row()
		if bs.has_server_object == True:
			search.enabled = False
		else:
			search.enabled = True
		search.prop_search(bs, "server_object", sc, "objects", text="", icon='OBJECT_DATAMODE')
		row = layout.row()
		row.operator("blive.logic_add", text="add logic")
		row.operator("blive.logic_remove", text="del logic")

###############################################
#
#	Network Setup Panel
#
###############################################

class BLive_PT_network_setup(bpy.types.Panel):
	bl_label = "BLive Network"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"

	#~ @classmethod
	#~ def poll(self, context):
		#~ """
			#~ test logic setup
		#~ """
		#~ sc = context.scene
		#~ return sc.blive_scene_settings.has_server_object

	def draw(self, context):
		layout = self.layout
		bs = context.window_manager.blive_settings
		server = bs.server
		port = bs.server
		
		row = layout.row()
		row.label("create logic and save blendfile before connect!")
		row = layout.row()
		row.operator("blive.fork_blenderplayer", text="start blenderplayer")
		row = layout.row()
		row.operator("blive.osc_connect", text="connect")
		row = layout.row()
		row.operator("blive.osc_quit", text="quit")

def register():
	print("settings.ui.register")
	bpy.utils.register_class(BLive_PT_common_settings)
	bpy.utils.register_class(BLive_PT_scene_settings)
	bpy.utils.register_class(BLive_PT_network_setup)

def unregister():
	print("settings.ui.unregister")
	bpy.utils.unregister_class(BLive_PT__common_settings)
	bpy.utils.unregister_class(BLive_PT_scene_settings)
	bpy.utils.unregister_class(BLive_PT_network_setup)
