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

import os
import bpy
from .. import client

class BLive_OT_videotexture_filebrowser(bpy.types.Operator):
	bl_idname = "blive.videotexture_filebrowser"
	bl_label = "BLive Videotexture Filebrowser"
	bl_options = {'REGISTER', 'UNDO'}
	
	filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filename = bpy.props.StringProperty()
	files = bpy.props.CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
	directory = bpy.props.StringProperty(subtype='DIR_PATH')
	use_filter_movie = bpy.props.BoolProperty(default=True)
	use_filter = bpy.props.BoolProperty(default=True)

	@classmethod
	def poll(self, context):
		try:
			return bool(context.active_object.active_material.active_texture.image)
		except AttributeError:
			return False

	def execute(self, context):
		ob = context.active_object
		image = ob.active_material.active_texture.image
		player = image.player

		if not player.has_playlist:
			client.client().send("/texture/movie", [ob.name, image.name, self.filepath, int(player.loop)])
		else:
			entry = player.playlist.add()
			entry.name = os.path.basename(self.filepath)
			entry.m_filepath = self.filepath

		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}


class BLive_OT_videotexture_play(bpy.types.Operator):
	bl_idname = "blive.videotexture_play"
	bl_label = "BLive Videotexture Play"

	@classmethod
	def poll(self, context):
		try:
			return bool(context.active_object.active_material.active_texture.image)
		except AttributeError:
			return False

	def execute(self, context):
		ob = context.active_object
		image = ob.active_material.active_texture.image
		player = image.player
		
		if player.has_playlist and player.playlist_entry_changed:
			client.client().send("/texture/movie", [ob.name, image.name, player.playlist[player.active_playlist_entry].m_filepath, int(player.loop)])
			player.playlist_entry_changed=False

		client.client().send("/texture/state", [ob.name, image.name, 'PLAY'])
		return {'FINISHED'}


class BLive_OT_videotexture_pause(bpy.types.Operator):
	bl_idname = "blive.videotexture_pause"
	bl_label = "BLive Videotexture Pause"

	@classmethod
	def poll(self, context):
		try:
			return bool(context.active_object.active_material.active_texture.image)
		except AttributeError:
			return False

	def execute(self, context):
		ob = context.active_object
		image = ob.active_material.active_texture.image
		client.client().send("/texture/state", [ob.name, image.name, 'PAUSE'])
		return {'FINISHED'}

class BLive_OT_videotexture_stop(bpy.types.Operator):
	bl_idname = "blive.videotexture_stop"
	bl_label = "BLive Videotexture Stop"

	@classmethod
	def poll(self, context):
		try:
			return bool(context.active_object.active_material.active_texture.image)
		except AttributeError:
			return False

	def execute(self, context):
		ob = bpy.context.object
		image = ob.active_material.active_texture.image
		player = image.player
		client.client().send("/texture/state", [ob.name, image.name, 'STOP'])
		player.playlist_entry_changed = True
		return {'FINISHED'}


def register():
	print("texture.ops.register")
	bpy.utils.register_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.register_class(BLive_OT_videotexture_pause)
	bpy.utils.register_class(BLive_OT_videotexture_play)
	bpy.utils.register_class(BLive_OT_videotexture_stop)
	
def unregister():
	print("texture.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.unregister_class(BLive_OT_videotexture_pause)
	bpy.utils.unregister_class(BLive_OT_videotexture_play)
	bpy.utils.unregister_class(BLive_OT_videotexture_stop)
