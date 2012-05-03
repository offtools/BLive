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
import sys
import subprocess
from . import client

###############################################
#
#	Scene Network Panel
#
###############################################

class BLive_PT_scene_network(bpy.types.Panel):
	bl_label = "BLive Network"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def draw(self, context):
		self.layout.label(text="Setup")

		box = self.layout.box()

		if "PORT" in bpy.context.scene.camera.game.properties:
			row = box.row()
			row.prop(bpy.context.scene.camera.game.properties["PORT"], "value", text="Port: ")
			row.operator("blive.set_port", text="change port")
			row.operator("blive.logic_remove", text="", icon="X")
		else:
			box.label("add OSC logic to: {}".format(bpy.context.scene.camera.name))
			row = box.row()
			row.operator("blive.logic_add", text="create scripts")
		
		if "PORT" not in bpy.context.scene.camera.game.properties:
			return
			
		row = self.layout.column()
		row.label("Next Steps:")

		row = self.layout.row()
		split = row.split(percentage=0.1)
		split.label("1.")
		split = split.split()
		split.operator_context = 'INVOKE_AREA'
		split.operator("wm.save_as_mainfile", text="Save As...")		
		
		row = self.layout.row()
		split = row.split(percentage=0.1)
		split.label("2.")
		split = split.split()
		if "PORT" not in bpy.context.scene.camera.game.properties or not bpy.context.blend_data.filepath:
			split.enabled = False		
		split.operator("blive.fork_blenderplayer", text="Start")
		
		row = self.layout.row()
		split = row.split(percentage=0.1)
		split.label("3.")
		split = split.split()
		split.operator("blive.quit", text="Quit")

class BLive_OT_forc_blenderplayer(bpy.types.Operator):
	bl_idname = "blive.fork_blenderplayer"
	bl_label = "BLive fork blenderplayer"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			client.client().port = bpy.context.scene.camera.game.properties["PORT"].value
			app = "blenderplayer"
			blendfile = bpy.context.blend_data.filepath
			port = "-p {0}".format(bpy.context.scene.camera.game.properties["PORT"].value)
			cmd = [app,  port, blendfile]
			blendprocess = subprocess.Popen(cmd)

			return{'FINISHED'}
		else:
			return{'CANCELLED'}

class BLive_OT_set_port(bpy.types.Operator):
	bl_idname = "blive.set_port"
	bl_label = "BLive set OSC port"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			client.client().port = bpy.context.scene.camera.game.properties["PORT"].value
			return{'FINISHED'}
		else:
			return{'CANCELLED'}

class BLive_OT_quit(bpy.types.Operator):
	bl_idname = "blive.quit"
	bl_label = "BLive quit blenderplayer"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			client.client().quit()
			# TODO unregister app handlers
			for i in bpy.app.handlers.frame_change_post:
				bpy.app.handlers.frame_change_post.remove(i)
			for i in bpy.app.handlers.scene_update_post:
				bpy.app.handlers.scene_update_post.remove(i)
			return{'FINISHED'}
		else:
			return{'CANCELLED'}

