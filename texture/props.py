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

def ImagePlayer_sourcetype_changed(self, context):
    #player = context.active_object.active_material.active_texture.image.player
    #player.source.filepath = ""
    pass

def ImageSource_source_changed(self, context):
    player = context.active_object.active_material.active_texture.image.player
    player.source_changed = True

class ImageSource(bpy.types.PropertyGroup):
    sourcetype = bpy.props.EnumProperty(items=( ("Movie","Movie",""),("Camera", "Camera",""),("Stream","Stream","") ), update=ImagePlayer_sourcetype_changed)
    filepath = bpy.props.StringProperty(default="", update=ImageSource_source_changed)
    audio = bpy.props.BoolProperty(default=False, update=ImageSource_source_changed)
    inpoint = bpy.props.FloatProperty(default=0, update=ImageSource_source_changed)
    outpoint = bpy.props.FloatProperty(default=0, update=ImageSource_source_changed)
    preseek = bpy.props.IntProperty(default=0, update=ImageSource_source_changed)
    loop = bpy.props.BoolProperty(default=False, update=ImageSource_source_changed)
    deinterlace = bpy.props.BoolProperty(default=False, update=ImageSource_source_changed)
    width = bpy.props.IntProperty(default=320, update=ImageSource_source_changed)
    height = bpy.props.IntProperty(default=240, update=ImageSource_source_changed)
    rate = bpy.props.FloatProperty(default=0.0, update=ImageSource_source_changed)

def ImagePlayer_entry_changed(self, context):
    player = context.active_object.active_material.active_texture.image.player
    player.entry_changed = True
    source = player.playlist[player.playlist_entry]
    player.source.sourcetype = source.sourcetype
    player.source.filepath = source.filepath
    player.source.audio = source.audio
    player.source.inpoint = source.inpoint
    player.source.outpoint = source.outpoint
    player.source.preseek = source.preseek
    player.source.loop = source.loop
    player.source.deinterlace = source.deinterlace
    player.source.width = source.width
    player.source.height = source.height
    player.source.rate = source.rate

state_enum =   (('PLAYING', 'Playing', 'Playing'),
                ('PAUSED', 'Paused', 'Paused'),
                ('STOPPED', 'Stopped', 'Stopped'),
                ('CLOSED', 'Closed', 'Closed')
                )

class ImagePlayer(bpy.types.PropertyGroup):
    '''
    Class: ImagePlayer
    control media playback on textures

    Method: get source
    returns the current source of type ImageSource,
    either a single source or playlist entry or None

    Attribute: mode
    play a single media source or use the playlist

    Attribute: playlist
    playlist, collection of ImageSource

    Attribute: source
    single media data, PointerProperty ImageSource

    Attribute: sourcetype
    enum in {"Movie","Stream","Camera"}

    Attribute: active_entry
    index of the active playlist entry
    '''

    mode = bpy.props.EnumProperty(name="mode", items=(("single","Single Media",""),("playlist","Playlist","")))
    playlist = bpy.props.CollectionProperty(type=ImageSource)
    source = bpy.props.PointerProperty(type=ImageSource)
    source_changed = bpy.props.BoolProperty(default=False)
    state = bpy.props.EnumProperty(name='ID Type', items=state_enum, default='CLOSED')
    playlist_entry = bpy.props.IntProperty(default=0, update=ImagePlayer_entry_changed)

def register():
    print("texture.props.register")
    bpy.utils.register_class(ImageSource)
    bpy.utils.register_class(ImagePlayer)
    bpy.types.Image.player = bpy.props.PointerProperty(type=ImagePlayer)

def unregister():
    print("texture.props.unregister")
    bpy.utils.unregister_class(ImagePlayer)
    bpy.utils.unregister_class(ImageSource)
