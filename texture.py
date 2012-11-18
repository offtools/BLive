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
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, EnumProperty
from . import client


def update_playlist(self, context):
	image = bpy.context.object.active_material.active_texture.image
	image.playlist_entry_changed = True

class ImagePlaylistEntry(bpy.types.PropertyGroup):
	m_filepath = bpy.props.StringProperty()

class ImageExtProperties():
	def register():
		bpy.utils.register_class(ImagePlaylistEntry)
		
		bpy.types.Image.loop = bpy.props.BoolProperty(default=True)
		bpy.types.Image.has_playlist = bpy.props.BoolProperty(default=False)
		bpy.types.Image.playlist = bpy.props.CollectionProperty(type=ImagePlaylistEntry)
		bpy.types.Image.active_playlist_entry = bpy.props.IntProperty(update=update_playlist)
		bpy.types.Image.playlist_entry_changed = bpy.props.BoolProperty(default=False)

	def unregister():
		del bpy.types.Image.loop
		del bpy.types.Image.has_playlist
		del bpy.types.Image.playlist
		del bpy.types.Image.active_playlist_entry
		del bpy.types.Image.playlist_entry_changed
		
		bpy.utils.unregister_class(ImagePlaylistEntry)

class BLive_OT_videotexture_filebrowser(bpy.types.Operator):
	bl_idname = "blive.videotexture_filebrowser"
	bl_label = "BLive Videotexture Filebrowser"
	bl_options = {'REGISTER', 'UNDO'}
	
	filepath = StringProperty(subtype="FILE_PATH")
	filename = StringProperty()
	files = CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
	directory = StringProperty(subtype='DIR_PATH')
	use_filter_movie = BoolProperty(default=True)
	use_filter = BoolProperty(default=True)

	def execute(self, context):
		print(self.files, self.directory, self.filepath, self.filename)
		if "PORT" in bpy.context.scene.camera.game.properties:
			ob = bpy.context.object
			image = bpy.context.object.active_material.active_texture.image
			
			if not image.has_playlist:
				client.client().send("/texture/movie", [ob.name, image.name, self.filepath, int(image.loop)])
			else:
				entry = image.playlist.add()
				entry.name = os.path.basename(self.filepath)
				entry.m_filepath = self.filepath
				
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}


class BLive_OT_videotexture_play(bpy.types.Operator):
	bl_idname = "blive.videotexture_play"
	bl_label = "BLive Videotexture Play"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			ob = bpy.context.object
			image = bpy.context.object.active_material.active_texture.image
			
			if image.has_playlist and image.playlist_entry_changed:
				client.client().send("/texture/movie", [ob.name, image.name, image.playlist[image.active_playlist_entry].m_filepath, int(image.loop)])
				image.playlist_entry_changed=False

			client.client().send("/texture/state", [ob.name, image.name, 'PLAY'])
		return {'FINISHED'}


class BLive_OT_videotexture_pause(bpy.types.Operator):
	bl_idname = "blive.videotexture_pause"
	bl_label = "BLive Videotexture Pause"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			ob = bpy.context.object
			image = bpy.context.object.active_material.active_texture.image.name
			client.client().send("/texture/state", [ob.name, image, 'PAUSE'])
		return {'FINISHED'}


class BLive_OT_videotexture_stop(bpy.types.Operator):
	bl_idname = "blive.videotexture_stop"
	bl_label = "BLive Videotexture Stop"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			ob = bpy.context.object
			image = bpy.context.object.active_material.active_texture.image.name
			client.client().send("/texture/state", [ob.name, image, 'STOP'])
			image.playlist_entry_changed = True
		return {'FINISHED'}


def enumerate_images():
	image_list = list()
	for index,image in enumerate(bpy.data.images):
		image_list.append((str(index), image.name, image.name))
	bpy.context.object['images'] = bpy.props.EnumProperty(items=image_list, default='-1')

class BLive_PT_texture_player(bpy.types.Panel):
	bl_label = "BLive Videoplayer"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "texture"

	@classmethod
	def poll(self, context):
		try:
			return bool(bpy.context.object.active_material.active_texture.image)
		except AttributeError:
			return False

	def draw(self, context):
		row = self.layout.row(align=True)
		row.alignment = 'EXPAND'
		row.operator("blive.videotexture_filebrowser", text="", icon="FILESEL")
		row.operator("blive.videotexture_play", text="", icon="PLAY")
		row.operator("blive.videotexture_pause", text="", icon="PAUSE")
		row.operator("blive.videotexture_stop", text="", icon="MESH_PLANE")

		row = self.layout.row(align=True)
		image = bpy.context.object.active_material.active_texture.image
		row.prop(image, "loop", text="loop video")
		row.prop(image, "has_playlist", text="use playlist")

		if image.has_playlist:
			row = self.layout.row(align=True)
			row.template_list(image, "playlist", image, "active_playlist_entry", rows=2, maxrows=8)

def register():
	print("texture.register")
	bpy.utils.register_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.register_class(BLive_OT_videotexture_pause)
	bpy.utils.register_class(BLive_OT_videotexture_play)
	bpy.utils.register_class(BLive_OT_videotexture_stop)
	bpy.utils.register_class(BLive_PT_texture_player)	
	ImageExtProperties.register()
	
def unregister():
	print("texture.unregister")
	bpy.utils.unregister_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.unregister_class(BLive_OT_videotexture_pause)
	bpy.utils.unregister_class(BLive_OT_videotexture_play)
	bpy.utils.unregister_class(BLive_OT_videotexture_stop)
	bpy.utils.unregister_class(BLive_PT_texture_player)	
	ImageExtProperties.unregister()
