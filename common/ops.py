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
import os
import sys
import subprocess
from ..client import BLiveClient

# TODO: test blenderplayer port cmdline options

class BLive_OT_logic_add(bpy.types.Operator):
	"""
		Operator - creates gamelogic used by osc server in gameengine
	"""
	bl_idname = "blive.logic_add"
	bl_label = "BLive - create logic brick"
	
	@classmethod
	def poll(self, context):
		"""
			test server_object is set and exists
		"""
		sc = context.scene
		bs = sc.blive_scene_settings
		#~ if not bs.server_object in sc.objects:
			#~ return True
		return bool(bs.server_object) and bs.server_object in sc.objects

	def execute(self, context):
		if not 'main.py' in bpy.data.texts:
			self.add_script()
		self.add_gamelogic(context)
		return{'FINISHED'} 

	def add_gamelogic(self, context):
		'''
			create gamelogic bricks 
		'''

		sc = context.scene
		bs = sc.blive_scene_settings
		server_object = sc.objects[bs.server_object]
		context.scene.objects.active = server_object

		if not 's.init' in context.active_object.game.sensors:
			bpy.ops.logic.sensor_add(type='ALWAYS', name='s.init')
		context.active_object.game.sensors['s.init'].use_pulse_true_level = False
		context.active_object.game.sensors['s.init'].use_pulse_false_level = False

		if not 's.update' in context.active_object.game.sensors:
			bpy.ops.logic.sensor_add(type='ALWAYS', name='s.update')
		context.active_object.game.sensors['s.update'].use_pulse_true_level = True
		context.active_object.game.sensors['s.update'].use_pulse_false_level = False
		context.active_object.game.sensors['s.update'].frequency = 0

		if not 'c.init' in context.active_object.game.controllers:
			bpy.ops.logic.controller_add(type='PYTHON', name='c.init')
		context.active_object.game.controllers['c.init'].mode = 'MODULE'
		context.active_object.game.controllers['c.init'].module = "main.start"

		if not 'c.update' in context.active_object.game.controllers:
			bpy.ops.logic.controller_add(type='PYTHON', name='c.update')
		context.active_object.game.controllers['c.update'].mode = 'MODULE'
		context.active_object.game.controllers['c.update'].module = "main.update"

		context.active_object.game.sensors['s.init'].link(context.active_object.game.controllers['c.init'])	
		context.active_object.game.sensors['s.update'].link(context.active_object.game.controllers['c.update'])

		bs.has_server_object = True

	def add_script(self):
		'''
			add server script for bge, appends import path dynamicly
		'''

		filename = "main.py"
		tpl = "bgetemplate.tpl"
		paths = bpy.utils.script_paths()
		for i in paths:
			path = os.path.join(i, "addons")
			for j in bpy.path.module_names(path, True):
				if bpy.context.window_manager.addons['blive'].module in j[0]:
					bpy.data.texts.new(name=filename)

					directory = os.path.dirname(j[1])
					filepath = os.path.join(directory, tpl)
					file = open(filepath, 'r')
					
					# add import path
					textblock = bpy.data.texts[filename] 
					textblock.write("import sys\n")
					textblock.write("sys.path.append(r'{0}')\n".format(directory))

					for line in file:
						textblock.write(line)
					file.close()
					return
		#   TODO?: error handling
		print("Error: addon path not found")

class BLive_OT_logic_remove(bpy.types.Operator):
	bl_idname = "blive.logic_remove"
	bl_label = "BLive - remove logic brick"

	@classmethod
	def poll(self, context):
		"""
			test server_object is set and exists
		"""
		sc = context.scene
		bs = sc.blive_scene_settings
		return bool(bs.server_object) and bs.server_object in sc.objects

	def execute(self, context):
		sc = context.scene
		bs = sc.blive_scene_settings
		server_object = sc.objects[bs.server_object]
		context.scene.objects.active = server_object

		if "s.init" in context.active_object.game.sensors:
			bpy.ops.logic.sensor_remove(sensor="s.init")
		
		if "s.update" in context.active_object.game.sensors:
			bpy.ops.logic.sensor_remove(sensor="s.update")
	
		if "c.init" in context.active_object.game.controllers:
			bpy.ops.logic.controller_remove(controller="c.init")
	
		if "c.update" in context.active_object.game.controllers:
			bpy.ops.logic.controller_remove(controller="c.update")
		
		bs.has_server_object = False

		return{'FINISHED'}

class BLive_OT_fork_blenderplayer(bpy.types.Operator):
	bl_idname = "blive.fork_blenderplayer"
	bl_label = "BLive fork blenderplayer"

	@classmethod
	def poll(self, context):
		"""
			test logic setup
		"""
		sc = context.scene
		return sc.blive_scene_settings.has_server_object

	def execute(self, context):
		sc = context.scene
		bs = sc.blive_scene_settings
		bc = context.window_manager.blive_settings
		server = bc.server
		port = bc.port
		
		app = "blenderplayer"
		blendfile = bpy.context.blend_data.filepath
		empty = '-'
		port = "-p {0}".format(port)
		cmd = [app,  blendfile, empty, port]
		blendprocess = subprocess.Popen(cmd)
		return{'FINISHED'}

class BLive_OT_osc_connect(bpy.types.Operator):
	bl_idname = "blive.osc_connect"
	bl_label = "connect to bge"

	@classmethod
	def poll(self, context):
		"""
			test logic setup
		"""
		sc = context.scene
		return sc.blive_scene_settings.has_server_object

	def execute(self, context):
		sc = context.scene
		bs = sc.blive_scene_settings
		bc = context.window_manager.blive_settings
		server = bc.server
		port = bc.port

		cli = BLiveClient()
		cli.connect(server, port)
		return{'FINISHED'}

class BLive_OT_osc_quit(bpy.types.Operator):
	bl_idname = "blive.osc_quit"
	bl_label = "BLive quit blenderplayer"

	@classmethod
	def poll(self, context):
		"""
			test logic setup
		"""
		sc = context.scene
		return sc.blive_scene_settings.has_server_object

	def execute(self, context):
		BLiveClient().quit()
		return{'FINISHED'}

def register():
	print("settings.ops.register")
	bpy.utils.register_class(BLive_OT_logic_add)
	bpy.utils.register_class(BLive_OT_logic_remove)
	bpy.utils.register_class(BLive_OT_fork_blenderplayer)
	bpy.utils.register_class(BLive_OT_osc_connect)
	bpy.utils.register_class(BLive_OT_osc_quit)

def unregister():
	print("settings.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_logic_add)
	bpy.utils.unregister_class(BLive_OT_logic_remove)
	bpy.utils.unregister_class(BLive_OT_fork_blenderplayer)
	bpy.utils.unregister_class(BLive_OT_osc_connect)
	bpy.utils.unregister_class(BLive_OT_osc_quit)
