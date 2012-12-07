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

class ImagePlaylistEntry(bpy.types.PropertyGroup):
	filepath = bpy.props.StringProperty()
	audio = bpy.props.BoolProperty(default=False)
	inpoint = bpy.props.FloatProperty(default=0)
	outpoint = bpy.props.FloatProperty(default=0)
	preseek = bpy.props.IntProperty(default=0)
	loop = bpy.props.BoolProperty(default=False)
	deinterlace = bpy.props.BoolProperty(default=False)

def playlist_entry_changed(self, context):
	player = context.active_object.active_material.active_texture.image.player
	player.playlist_entry_changed = True

class ImagePlayer(bpy.types.PropertyGroup):
	loop = bpy.props.BoolProperty(default=True)
	has_playlist = bpy.props.BoolProperty(default=False)
	playlist = bpy.props.CollectionProperty(type=ImagePlaylistEntry)
	active_playlist_entry = bpy.props.IntProperty(default=-1, update=playlist_entry_changed)
	playlist_entry_changed = bpy.props.BoolProperty(default=True)
	audio = bpy.props.BoolProperty(default=False)

def register():
	print("texture.props.register")
	bpy.utils.register_class(ImagePlaylistEntry)
	bpy.utils.register_class(ImagePlayer)
	bpy.types.Image.player = bpy.props.PointerProperty(type=ImagePlayer)

def unregister():
	print("texture.props.unregister")
	bpy.utils.unregister_class(ImagePlayer)
	bpy.utils.unregister_class(ImagePlaylistEntry)