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

# TODO: *add proper poll methods

import os
import bpy
from liblo import Bundle, Message
from ..common.libloclient import Client
from .props import ImageSource

#
# --- Operators used by gui (works on active object)
# --- Wrapper for osc Operators
#

class BLive_OT_videotexture_play(bpy.types.Operator):
    '''Videotexture play'''

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

        if not len(player.playlist):
            return{'CANCELLED'}

        if not player.selected_playlist_entry == player.active_playlist_entry:
            # open new media
            entry = player.playlist[player.selected_playlist_entry]
            if entry.sourcetype == 'Movie':
                bpy.ops.blive.osc_videotexture_open_movie(  obname=ob.name,
                                                            imgname=image.name,
                                                            filepath=entry.filepath,
                                                            audio=entry.audio,
                                                            inpoint=entry.inpoint,
                                                            outpoint=entry.outpoint,
                                                            loop=entry.loop,
                                                            preseek=entry.preseek,
                                                            deinterlace=entry.deinterlace
                                                         )
            elif entry.sourcetype == 'Camera':
                pass
            elif entry.sourcetype == 'Stream':
                bpy.ops.blive.osc_videotexture_open_movie(  obname=ob.name,
                                                            imgname=image.name,
                                                            filepath=entry.filepath,
                                                            audio=entry.audio,
                                                            inpoint=0.0,
                                                            outpoint=0.0,
                                                            loop=False,
                                                            preseek=0,
                                                            deinterlace=False
                                                         )
            player.active_playlist_entry = player.selected_playlist_entry

        else:
            bpy.ops.blive.osc_videotexture_play(imgname=image.name)

        image.player.state = 'PLAYING'
        return {'FINISHED'}

class BLive_OT_videotexture_pause(bpy.types.Operator):
    '''Videotexture pause'''
    bl_idname = "blive.videotexture_pause"
    bl_label = "BLive Videotexture Pause"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        image = context.active_object.active_material.active_texture.image
        bpy.ops.blive.osc_videotexture_pause(imgname=image.name)
        image.player.state = 'PAUSED'
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
        image = context.active_object.active_material.active_texture.image
        bpy.ops.blive.osc_videotexture_stop(imgname=image.name)
        image.player.state = 'STOPPED'
        return {'FINISHED'}

class BLive_OT_videotexture_close(bpy.types.Operator):
    bl_idname = "blive.videotexture_close"
    bl_label = "BLive Reset Videotexture"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        image = context.active_object.active_material.active_texture.image
        bpy.ops.blive.osc_videotexture_close(imgname=image.name)
        image.player.state = 'CLOSED'
        image.player.active_playlist_entry = -1
        return {'FINISHED'}

class BLive_OT_videotexture_playlist_add_entry(bpy.types.Operator):
    '''Videotexture add playlist entry'''
    bl_idname = "blive.videotexture_playlist_add_entry"
    bl_label = "BLive add playlist entry"
    uri = bpy.props.StringProperty()

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

        if player.sourcetype == 'Movie':
            if 'FILE_BROWSER' in [i.type for i in context.screen.areas]:
                narea = [i.type for i in context.screen.areas].index('FILE_BROWSER')
                nspace = [i.type for i in context.screen.areas[narea].spaces].index('FILE_BROWSER')
                space = context.screen.areas[narea].spaces[nspace]
                filename = space.params.filename
                directory = space.params.directory
                if filename:
                    filepath = "{0}/{1}".format(directory, filename)
                    entry = player.playlist.add()
                    entry.name = filename
                    entry.filepath = filepath
                    entry.sourcetype = player.sourcetype
            else:
                return{'CANCELLED'}
        elif player.sourcetype == 'Camera' or player.sourcetype == 'Stream':
            entry = player.playlist.add()
            entry.name = self.uri
            entry.filepath = self.uri
            entry.sourcetype = player.sourcetype

        # select currently added entry
        player.selected_playlist_entry = len(player.playlist) - 1

        return {'FINISHED'}

    def invoke(self, context, event):
        image = context.active_object.active_material.active_texture.image
        player = image.player
        if not player.sourcetype == 'Movie':
            return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)

    def draw(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.sourcetype == 'Camera':
            self.layout.label("Camera Device Path")
            row = self.layout.row()
            row.prop(self, "uri", text='')
        elif player.sourcetype == 'Stream':
            self.layout.label("Stream URI")
            row = self.layout.row()
            row.prop(self, "uri", text='')

class BLive_OT_videotexture_playlist_move_entry_up(bpy.types.Operator):
    '''Videotexture move playlist entry up'''
    bl_idname = "blive.videotexture_playlist_move_entry_up"
    bl_label = "BLive move playlist entry up"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.selected_playlist_entry > 0 and player.selected_playlist_entry < len(player.playlist):
            player.playlist.move(player.selected_playlist_entry, player.selected_playlist_entry - 1)
            player.selected_playlist_entry = player.selected_playlist_entry - 1
            return{'FINISHED'}
        else:
            return{'CANCELLED'}


class BLive_OT_videotexture_playlist_move_entry_down(bpy.types.Operator):
    '''Videotexture move playlist entry down'''
    bl_idname = "blive.videotexture_playlist_move_entry_down"
    bl_label = "BLive move playlist entry down"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.selected_playlist_entry > -1 and player.selected_playlist_entry < len(player.playlist) - 1:
            player.playlist.move(player.selected_playlist_entry, player.selected_playlist_entry + 1)
            player.selected_playlist_entry = player.selected_playlist_entry + 1
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_videotexture_playlist_delete_entry(bpy.types.Operator):
    '''Videotexture delete playlist entry'''
    bl_idname = "blive.videotexture_playlist_delete_entry"
    bl_label = "BLive delete playlist entry"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.selected_playlist_entry < len(player.playlist):
            bpy.ops.blive.videotexture_close()
            player.playlist.remove(player.selected_playlist_entry)
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_videotexture_playlist_next_entry(bpy.types.Operator):
    '''Videotexture goto next playlist entry'''
    bl_idname = "blive.videotexture_playlist_next_entry"
    bl_label = "BLive next playlist entry"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.selected_playlist_entry < len(player.playlist) - 1:
            player.selected_playlist_entry = player.selected_playlist_entry + 1
            #player.state = 'CHANGED'
            bpy.ops.blive.videotexture_play()
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_videotexture_playlist_prev_entry(bpy.types.Operator):
    '''Videotexture goto prev playlist entry'''
    bl_idname = "blive.videotexture_playlist_prev_entry"
    bl_label = "BLive prev playlist entry"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        player = context.active_object.active_material.active_texture.image.player

        if player.selected_playlist_entry > 0:
            player.selected_playlist_entry = player.selected_playlist_entry - 1
            #player.state = 'CHANGED'
            bpy.ops.blive.videotexture_play()
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_videotexture_mixer_popup(bpy.types.Operator):
    '''Videotexture mixer dialog'''
    bl_idname = "blive.videotexture_mixer_popup"
    bl_label = "BLive videotexture mixer"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
            return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=400)

    def draw(self, context):
        layout = self.layout
        for ob in bpy.data.objects:
            image = None
            for matslots in ob.material_slots:
                for texslots in matslots.material.texture_slots:
                    if hasattr(texslots, 'texture') and hasattr(texslots.texture, 'image'):
                        image = texslots.texture.image
            if image and not image.player.state == 'CLOSED':
                row = layout.row()
                row.label(ob.name, icon='OBJECT_DATA')
                row.label(image.name, icon='IMAGE_DATA')
                filename = os.path.basename(image.player.playlist[image.player.selected_playlist_entry].filepath)
                row.label(filename, icon='FILE_MOVIE')
                box = layout.box()
                row = box.row(align=True)
                row.prop(ob, 'color', text='Alpha', index=3)
                row = box.row()
                row.prop(image.player, 'volume', text='Volume')
                layout.separator()

#
# --- Client OSC Operators
#

#
# --- Operators for Movies
#
class BLive_OT_osc_videotexture_open_movie(bpy.types.Operator):
    '''open a movie file for a videotexture'''
    bl_idname = "blive.osc_videotexture_open_movie"
    bl_label = "BLive Open Moviefile"

    obname = bpy.props.StringProperty()
    imgname = bpy.props.StringProperty()
    filepath = bpy.props.StringProperty()
    audio = bpy.props.BoolProperty(default=False)
    inpoint = bpy.props.FloatProperty(default=0.0)
    outpoint = bpy.props.FloatProperty(default=0.0)
    loop = bpy.props.BoolProperty(default=False)
    preseek = bpy.props.FloatProperty(default=0)
    deinterlace = bpy.props.BoolProperty(default=False)

    #~ @classmethod
    #~ def poll(self, context):
        #~ return self.obname in context.scene.objects and self.imgname in bpy.data.images

    def execute(self, context):
        Client().send(Message("/bge/logic/media/openMovie",
                            self.obname,
                            self.imgname,
                            self.filepath,
                            int(self.audio),
                            self.inpoint,
                            self.outpoint,
                            int(self.loop),
                            self.preseek,
                            int(self.deinterlace))
                            )

        return {'FINISHED'}

class BLive_OT_osc_videotexture_enable_audio(bpy.types.Operator):
    '''enable audio for Videotexture'''
    bl_idname = "blive.osc_videotexture_enable_audio"
    bl_label = "BLive enable Audio for Videotexture"

    imgname = bpy.props.StringProperty()
    audio = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        Client().send(Message("/bge/logic/media/enableAudio",
                            self.imgname,
                            int(self.audio)
                            ))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_set_range(bpy.types.Operator):
    '''set in and outpoints for moviefile'''
    bl_idname = "blive.osc_videotexture_set_range"
    bl_label = "BLive set Movie In- and Outpoints"

    imgname = bpy.props.StringProperty()
    inp = bpy.props.FloatProperty(default=0.0)
    outp = bpy.props.FloatProperty(default=0.0)

    def execute(self, context):
        Client().send(Message("/bge/logic/media/setRange",
                            self.imgname,
                            self.inp, self.outp
                            ))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_set_volume(bpy.types.Operator):
    '''set volume for movie file'''
    bl_idname = "blive.osc_videotexture_set_volume"
    bl_label = "BLive set Volume"

    imgname = bpy.props.StringProperty()
    volume = bpy.props.FloatProperty(default=1.0)

    def execute(self, context):
        Client().send(Message("/bge/logic/media/audioVolume",
                            self.imgname,
                            self.volume
                            ))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_enable_loop(bpy.types.Operator):
    '''loop videotexture movie playback'''
    bl_idname = "blive.osc_videotexture_enable_loop"
    bl_label = "BLive Loop Movie"

    imgname = bpy.props.StringProperty()
    loop = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        Client().send(Message("/bge/logic/media/enableLoop",
                            self.imgname,
                            int(self.loop)
                            ))
        return {'FINISHED'}

##
## --- Operators for Camera
##
#class BLive_OT_osc_camera_open(bpy.types.Operator):
    #'''
        #OSC Command: open a camera device and play it on a texture
        #bpy.ops.blive.osc_camera_open(obname='object', imgname='image', device=0, width=320, height=240, rate=25, deinterlace=False)
    #'''
    #bl_idname = "blive.osc_camera_open"
    #bl_label = "BLive Open Camera Device"

    #obname = bpy.props.StringProperty()
    #imgname = bpy.props.StringProperty()
    #filepath = bpy.props.StringProperty()
    #width = bpy.props.IntProperty(default=320)
    #height = bpy.props.IntProperty(default=240)
    #rate = bpy.props.IntProperty(default=25)
    #deinterlace = bpy.props.BoolProperty(default=False)

    #def execute(self, context):
        #BLiveClient().send("/texture/camera/open", [
                            #self.obname,
                            #self.imgname,
                            #self.filepath,
                            #self.width,
                            #self.height,
                            #self.rate,
                            #int(self.deinterlace) ]
                            #)

        #return {'FINISHED'}

#
# --- Videotexture Status Operators (Controls)
#
class BLive_OT_osc_videotexture_close(bpy.types.Operator):
    '''close videotexture'''
    bl_idname = "blive.osc_videotexture_close"
    bl_label = "BLive Close videotexture"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/close", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_play(bpy.types.Operator):
    '''play videotexture'''
    bl_idname = "blive.osc_videotexture_play"
    bl_label = "BLive Start Playback"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/play", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_pause(bpy.types.Operator):
    '''pause videotexture playback'''
    bl_idname = "blive.osc_videotexture_pause"
    bl_label = "BLive Pause Videotexture Playback"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/pause", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_stop(bpy.types.Operator):
    '''stop Videotexture playback'''
    bl_idname = "blive.osc_videotexture_stop"
    bl_label = "BLive Stop Videotexture Playback"
    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/stop", self.imgname))
        return {'FINISHED'}

#
# --- Videotexture Filter Operators
#
class BLive_OT_osc_videotexture_deinterlace(bpy.types.Operator):
    '''enable videotexture deinterlacing'''
    bl_idname = "blive.osc_videotexture_deinterlace"
    bl_label = "BLive Deinterlace Videotexture"

    imgname = bpy.props.StringProperty()
    deinterlace = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        Client().send(Message("/bge/logic/media/deinterlace",
                            self.imgname,
                            int(self.deinterlace)
                            ))
        return {'FINISHED'}


def register():
    print("texture.ops.register")
    #bpy.utils.register_class(BLive_OT_videotexture_filebrowser)
    #bpy.utils.register_class(BLive_OT_videotexture_open)
    bpy.utils.register_class(BLive_OT_videotexture_pause)
    bpy.utils.register_class(BLive_OT_videotexture_play)
    bpy.utils.register_class(BLive_OT_videotexture_stop)
    bpy.utils.register_class(BLive_OT_videotexture_close)
    bpy.utils.register_class(BLive_OT_videotexture_mixer_popup)

    bpy.utils.register_class(BLive_OT_videotexture_playlist_add_entry)
    bpy.utils.register_class(BLive_OT_videotexture_playlist_delete_entry)
    bpy.utils.register_class(BLive_OT_videotexture_playlist_next_entry)
    bpy.utils.register_class(BLive_OT_videotexture_playlist_prev_entry)
    bpy.utils.register_class(BLive_OT_videotexture_playlist_move_entry_up)
    bpy.utils.register_class(BLive_OT_videotexture_playlist_move_entry_down)

    bpy.utils.register_class(BLive_OT_osc_videotexture_open_movie)
    bpy.utils.register_class(BLive_OT_osc_videotexture_enable_audio)
    bpy.utils.register_class(BLive_OT_osc_videotexture_set_volume)
    bpy.utils.register_class(BLive_OT_osc_videotexture_set_range)
    bpy.utils.register_class(BLive_OT_osc_videotexture_enable_loop)

    #bpy.utils.register_class(BLive_OT_osc_camera_open)

    bpy.utils.register_class(BLive_OT_osc_videotexture_close)
    bpy.utils.register_class(BLive_OT_osc_videotexture_play)
    bpy.utils.register_class(BLive_OT_osc_videotexture_pause)
    bpy.utils.register_class(BLive_OT_osc_videotexture_stop)
    bpy.utils.register_class(BLive_OT_osc_videotexture_deinterlace)

def unregister():
    print("texture.ops.unregister")
    #bpy.utils.unregister_class(BLive_OT_videotexture_filebrowser)
    #bpy.utils.unregister_class(BLive_OT_videotexture_open)
    bpy.utils.unregister_class(BLive_OT_videotexture_pause)
    bpy.utils.unregister_class(BLive_OT_videotexture_play)
    bpy.utils.unregister_class(BLive_OT_videotexture_stop)
    bpy.utils.unregister_class(BLive_OT_videotexture_close)
    bpy.utils.unregister_class(BLive_OT_videotexture_mixer_popup)

    bpy.utils.unregister_class(BLive_OT_videotexture_playlist_add_entry)
    bpy.utils.unregister_class(BLive_OT_videotexture_playlist_delete_entry)
    bpy.utils.unregister_class(BLive_OT_videotexture_playlist_next_entry)
    bpy.utils.unregister_class(BLive_OT_videotexture_playlist_prev_entry)

    #bpy.utils.unregister_class(BLive_OT_osc_camera_open)

    bpy.utils.unregister_class(BLive_OT_osc_videotexture_open_movie)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_enable_audio)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_set_volume)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_set_range)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_enable_loop)

    bpy.utils.unregister_class(BLive_OT_osc_videotexture_close)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_play)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_pause)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_stop)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_deinterlace)
