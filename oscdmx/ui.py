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

class BLive_PT_network_dmx_over_osc(bpy.types.Panel):
	bl_label = "BLive DMX over OSC"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	
	@classmethod
	def poll(self, context):
		return context.window_manager.blive_settings.use_dmx_over_osc

	def draw(self, context):
		layout = self.layout
		bs = context.window_manager.blive_settings
		row = layout.row()
		row.label("receive dmx as OSC Messages")

def register():
	print("oscdmx.ui.register")
	bpy.utils.register_class(BLive_PT_network_dmx_over_osc)

def unregister():
	print("oscdmx.ui.unregister")
	bpy.utils.unregister_class(BLive_PT_network_dmx_over_osc)
