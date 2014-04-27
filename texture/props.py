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

class ImageSource(bpy.types.PropertyGroup):
    sourcetype = bpy.props.EnumProperty(items=( ("Movie","Movie",""),("Camera", "Camera",""),("Stream","Stream","") ))
    filepath = bpy.props.StringProperty(default="")
    audio = bpy.props.BoolProperty(default=False)
    inpoint = bpy.props.FloatProperty(default=0)
    outpoint = bpy.props.FloatProperty(default=0)
    preseek = bpy.props.IntProperty(default=0)
    loop = bpy.props.BoolProperty(default=False)
    deinterlace = bpy.props.BoolProperty(default=False)
    volume = bpy.props.FloatProperty(default=1.0, min=0.0, max=1.0)
    width = bpy.props.IntProperty(default=320)
    height = bpy.props.IntProperty(default=240)
    rate = bpy.props.FloatProperty(default=0.0)
    follow = bpy.props.EnumProperty(name="follow", items=(("reset","Reset Texture",""),("hold","hold last Image",""), ("next", "goto next Entry", "")))

state_enum =   (('PLAYING', 'Playing', 'Playing'),
                ('PAUSED', 'Paused', 'Paused'),
                ('STOPPED', 'Stopped', 'Stopped'),
                ('CLOSED', 'Closed', 'Closed'),
#                ('CHANGED', 'Changed', 'Changed'),
                )

class ImagePlayer(bpy.types.PropertyGroup):
    '''
    Class: ImagePlayer
    control media playback on textures
    '''
    sourcetype = bpy.props.EnumProperty(items=( ("Movie","Movie",""),("Camera", "Camera",""),("Stream","Stream","") ) )

    # playlist
    playlist = bpy.props.CollectionProperty(type=ImageSource)

    ## selected playlist entry
    selected_playlist_entry = bpy.props.IntProperty(default=0)

    ## currently played playlist entry
    active_playlist_entry = bpy.props.IntProperty(default=-1)

    # controls
    state = bpy.props.EnumProperty(name='ID Type', items=state_enum, default='CLOSED')

    # FIX: enabling sound during forces restart of the video
    #def controls_audio(self, context):
        #image = context.active_object.active_material.active_texture.image
        #bpy.ops.blive.osc_videotexture_enable_audio(imgname=image.name, audio=int(self.audio))

    #audio = bpy.props.BoolProperty(default=False, update=controls_audio)

    def loop_updated(self, context):
        image = context.active_object.active_material.active_texture.image
        bpy.ops.blive.osc_videotexture_enable_loop(imgname=image.name, loop=int(self.loop))

    loop = bpy.props.BoolProperty(default=False, update=loop_updated)

    def volume_updated(self, context):
        image = context.active_object.active_material.active_texture.image
        bpy.ops.blive.osc_videotexture_set_volume(imgname=image.name, volume=self.volume)

    volume = bpy.props.FloatProperty(default=1.0, min=0.0, max=1.0, update=volume_updated)

def register():
    print("texture.props.register")
    bpy.utils.register_class(ImageSource)
    bpy.utils.register_class(ImagePlayer)
    bpy.types.Image.player = bpy.props.PointerProperty(type=ImagePlayer)

def unregister():
    print("texture.props.unregister")
    bpy.utils.unregister_class(ImagePlayer)
    bpy.utils.unregister_class(ImageSource)
