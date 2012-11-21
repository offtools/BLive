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

def enumerate_images():
	image_list = list()
	for index,image in enumerate(bpy.data.images):
		image_list.append((str(index), image.name, image.name))
	bpy.context.object['images'] = bpy.props.EnumProperty(items=image_list, default=0)

class BLive_PT_texture_player(bpy.types.Panel):
	bl_label = "BLive Videoplayer"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "texture"

	@classmethod
	def poll(self, context):
		try:
			return bool(context.active_object.active_material.active_texture.image)
		except AttributeError:
			return False

	def draw(self, context):
		ob = context.active_object
		image = ob.active_material.active_texture.image
		player = image.player

		row = self.layout.row(align=True)
		row.alignment = 'EXPAND'
		row.operator("blive.videotexture_filebrowser", text="", icon="FILESEL")
		row.operator("blive.videotexture_play", text="", icon="PLAY")
		row.operator("blive.videotexture_pause", text="", icon="PAUSE")
		row.operator("blive.videotexture_stop", text="", icon="MESH_PLANE")

		row = self.layout.row(align=True)
		row.prop(player, "loop", text="loop video")
		row.prop(player, "has_playlist", text="use playlist")

		if player.has_playlist:
			row = self.layout.row(align=True)
			row.template_list(player, "playlist", player, "active_playlist_entry", rows=2, maxrows=8)

def register():
	print("texture.ui.register")
	bpy.utils.register_class(BLive_PT_texture_player)	

def unregister():
	print("texture.ui.unregister")
	bpy.utils.unregister_class(BLive_PT_texture_player)	
