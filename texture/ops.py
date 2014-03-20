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
# every input is written to source in playlist mode source is copied to an new playlistentry and
# source is reset

# button [filename] ](open)(plus)(delete)

import os
import bpy
from liblo import Bundle, Message
from ..common.libloclient import Client
from .props import ImageSource

class BLive_OT_videotexture_source_from_filebrowser(bpy.types.Operator):
    '''select source media file from a filebrowser'''

    bl_idname = "blive.videotexture_source_from_filebrwoser"
    bl_label = "BLive Source from Filebrowser"

    @classmethod
    def poll(self, context):
        try:
            return bool(context.active_object.active_material.active_texture.image)
        except AttributeError:
            return False

    def execute(self, context):
        ob = context.active_object
        image = ob.active_material.active_texture.image
        source = image.player.source
        if 'FILE_BROWSER' in [i.type for i in context.screen.areas]:
            narea = [i.type for i in context.screen.areas].index('FILE_BROWSER')
            nspace = [i.type for i in context.screen.areas[narea].spaces].index('FILE_BROWSER')
            space = context.screen.areas[narea].spaces[nspace]
            filename = space.params.filename
            directory = space.params.directory
            if filename:
                source.filepath = "{0}/{1}".format(directory, filename)
                bpy.ops.blive.osc_movie_open(obname=ob.name,
                            imgname=image.name,
                            filepath=source.filepath,
                            audio=source.audio,
                            inpoint=source.inpoint,
                            outpoint=source.outpoint,
                            loop=source.loop,
                            preseek=source.preseek,
                            deinterlace=source.deinterlace
                            )
                return{'FINISHED'}
        return{'CANCELED'}

#
# --- Operators used by gui (works on active object)
# --- Wrapper for osc Operators
#
#class BLive_OT_videotexture_filebrowser(bpy.types.Operator):
    #bl_idname = "blive.videotexture_filebrowser"
    #bl_label = "BLive open Video Filebrowser"
    #bl_options = {'REGISTER', 'UNDO'}

    #filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    #filename = bpy.props.StringProperty()
    #files = bpy.props.CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
    #directory = bpy.props.StringProperty(subtype='DIR_PATH')
    #use_filter_movie = bpy.props.BoolProperty(default=True)
    #use_filter = bpy.props.BoolProperty(default=True)

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = context.active_object
        #image = ob.active_material.active_texture.image
        #source = image.player.source

        ## set filepath
        #source.filepath = self.filepath

        #return {'FINISHED'}

    #def invoke(self, context, event):
        #context.window_manager.fileselect_add(self)
        #return {'RUNNING_MODAL'}

#class BLive_OT_videotexture_open(bpy.types.Operator):
    #'''
        #sets Videotexture State to play, if used with playlist, the Operator
        #checks if a playlist entry is changed and opens a new playlist entry
    #'''
    #bl_idname = "blive.videotexture_open"
    #bl_label = "BLive Videotexture Open Media"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = context.active_object
        #image = ob.active_material.active_texture.image
        #player = image.player
        #source = player.source

        #if source.sourcetype == "Movie":
            #bpy.ops.blive.osc_movie_open(obname=ob.name,
                                        #imgname=image.name,
                                        #filepath=source.filepath,
                                        #audio=source.audio,
                                        #inpoint=source.inpoint,
                                        #outpoint=source.outpoint,
                                        #loop=source.loop,
                                        #preseek=source.preseek,
                                        #deinterlace=source.deinterlace
                                        #)

        #elif source.sourcetype == "Camera":
            #bpy.ops.blive.osc_camera_open(obname=ob.name,
                                                #imgname=image.name,
                                                #filepath=source.filepath,
                                                #width=source.width,
                                                #height=source.height,
                                                #rate=source.rate,
                                                #deinterlace=source.deinterlace )

        #elif source.sourcetype == "Stream":
            #bpy.ops.blive.osc_movie_open(obname=ob.name,
                                        #imgname=image.name,
                                        #filepath=source.filepath,
                                        #audio=source.audio,
                                        #loop=source.loop
                                        #)

        #return {'FINISHED'}

#class BLive_OT_videotexture_play(bpy.types.Operator):
    #'''
        #sets Videotexture State to play, if used with playlist, the Operator
        #checks if a playlist entry is changed and opens a new playlist entry
    #'''
    #bl_idname = "blive.videotexture_play"
    #bl_label = "BLive Videotexture Play"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #image = context.active_object.active_material.active_texture.image
        #player = image.player

        #if player.source_changed:
            #bpy.ops.blive.videotexture_open()
            #player.source_changed = False
        #else:
            #bpy.ops.blive.osc_videotexture_play(imgname=context.active_object.active_material.active_texture.image.name)

        #return {'FINISHED'}

#class BLive_OT_videotexture_pause(bpy.types.Operator):
    #bl_idname = "blive.videotexture_pause"
    #bl_label = "BLive Videotexture Pause"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #bpy.ops.blive.osc_videotexture_pause(imgname=context.active_object.active_material.active_texture.image.name)
        #return {'FINISHED'}

#class BLive_OT_videotexture_stop(bpy.types.Operator):
    #bl_idname = "blive.videotexture_stop"
    #bl_label = "BLive Videotexture Stop"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #bpy.ops.blive.osc_videotexture_stop(imgname=context.active_object.active_material.active_texture.image.name)
        ##player.entry_changed = True
        #return {'FINISHED'}

#class BLive_OT_videotexture_close(bpy.types.Operator):
    #bl_idname = "blive.videotexture_close"
    #bl_label = "BLive Reset Videotexture"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = bpy.context.object
        #image = ob.active_material.active_texture.image
        #player = image.player
        #bpy.ops.blive.osc_videotexture_close(imgname=image.name)
        ##player.entry_changed = True
        #return {'FINISHED'}

#class BLive_OT_videotexture_playlist_add(bpy.types.Operator):
    #'''
    #copy source properties into playlist
    #'''
    #bl_idname = "blive.videotexture_playlist_add"
    #bl_label = "BLive add Playlist Entry"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #image = context.active_object.active_material.active_texture.image
        #player = image.player
        #source = player.source

        #entry = image.player.playlist.add()
        #entry.name = source.filepath
        #entry.sourcetype = source.sourcetype
        #entry.filepath = source.filepath
        #entry.audio = source.audio
        #entry.inpoint = source.inpoint
        #entry.outpoint = source.outpoint
        #entry.preseek = source.preseek
        #entry.loop = source.loop
        #entry.deinterlace = source.deinterlace
        #entry.width = source.width
        #entry.height = source.height
        #entry.rate = source.rate

        #player.playlist_entry = len(player.playlist)-1

        #return {'FINISHED'}

#class BLive_OT_videotexture_playlist_remove(bpy.types.Operator):
    #bl_idname = "blive.videotexture_playlist_remove"
    #bl_label = "BLive Remove Playlist Entry"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = bpy.context.object
        #image = ob.active_material.active_texture.image
        #player = image.player
        #player.playlist.remove(player.playlist_entry)

        #return {'FINISHED'}

##
## --- Client OSC Operators
##

#
# --- Operators for Movies
#
class BLive_OT_osc_movie_open(bpy.types.Operator):
    '''
        OSC Command: open a movie and play it on a texture
        bpy.ops.blive.osc_movie_open(obname='object', imgname='image', filepath='path', audio='False', inpoint=0.0, outpoint=0.0, loop=False, preseek=0, deinterlace=False)
    '''
    bl_idname = "blive.osc_movie_open"
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

#class BLive_OT_osc_movie_audio(bpy.types.Operator):
    #'''
        #OSC Command: enable audio for Videotexture
        #bpy.ops.blive.osc_movie_audion(imgname='image')
    #'''
    #bl_idname = "blive.osc_movie_audio"
    #bl_label = "BLive enable Audio for Videotexture"

    #imgname = bpy.props.StringProperty()
    #audio = bpy.props.BoolProperty(default=False)

    #def execute(self, context):
        #BLiveClient().send("/texture/movie/audio", [
                            #self.imgname,
                            #self.audio ]
                            #)
        #return {'FINISHED'}

#class BLive_OT_osc_movie_range(bpy.types.Operator):
    #'''
        #OSC Command: set in and outpoints for moviefile
        #bpy.ops.blive.osc_movie_range(imgname='image')
    #'''
    #bl_idname = "blive.osc_movie_range"
    #bl_label = "BLive Set Movie In- and Outpoints"

    #imgname = bpy.props.StringProperty()
    #inp = bpy.props.FloatProperty(default=0.0)
    #outp = bpy.props.FloatProperty(default=0.0)

    #def execute(self, context):
        #BLiveClient().send("/texture/movie/audio", [
                            #self.imgname,
                            #self.inp, self.outp ]
                            #)
        #return {'FINISHED'}

#class BLive_OT_osc_movie_loop(bpy.types.Operator):
    #'''
        #OSC Command: loop videotexture movie playback
        #bpy.ops.blive.osc_movie_loop(imgname='image')
    #'''
    #bl_idname = "blive.osc_movie_loop"
    #bl_label = "BLive Loop Movie"

    #imgname = bpy.props.StringProperty()
    #loop = bpy.props.BoolProperty(default=False)

    #def execute(self, context):
        #BLiveClient().send("/texture/movie/loop", [
                            #self.imgname,
                            #int(self.loop) ]
                            #)
        #return {'FINISHED'}

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
    '''
        OSC Command: Close media and reset Texture
        blive.osc_videotexture_close(imgname='image')
    '''
    bl_idname = "blive.osc_videotexture_close"
    bl_label = "BLive Close videotexture"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/close", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_play(bpy.types.Operator):
    '''
        OSC Command: Videotexture Play
        blive.osc_videotexture_play(imgname='image')
    '''
    bl_idname = "blive.osc_videotexture_play"
    bl_label = "BLive Start Playback"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/play", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_pause(bpy.types.Operator):
    '''
        OSC Command: Videotexture Pause
        blive.osc_videotexture_pause(imgname='image')
    '''
    bl_idname = "blive.osc_videotexture_pause"
    bl_label = "BLive Pause Playback"

    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/pause", self.imgname))
        return {'FINISHED'}

class BLive_OT_osc_videotexture_stop(bpy.types.Operator):
    '''
        OSC Command: Videotexture Stop
        blive.osc_videotexture_play(imgname='image')
    '''
    bl_idname = "blive.osc_videotexture_stop"
    bl_label = "BLive Stop Playback"
    imgname = bpy.props.StringProperty()

    def execute(self, context):
        Client().send(Message("/bge/logic/media/stop", self.imgname))
        return {'FINISHED'}

##
## --- Videotexture Filter Operators
##
#class BLive_OT_osc_filter_deinterlace(bpy.types.Operator):
    #'''
        #OSC Command: Videotexture Stop
        #blive.osc_videotexture_play(imgname='image', deinterlace='False')
    #'''
    #bl_idname = "blive.osc_videotexture_filter"
    #bl_label = "BLive Deinterlace Videotexture"

    #imgname = bpy.props.StringProperty()
    #deinterlace = bpy.props.BoolProperty(default=False)

    #def execute(self, context):
        #BLiveClient().send("/texture/filter/deinterlace", [
                            #self.imgname,
                            #self.deinterlace ]
                            #)
        #return {'FINISHED'}

##
## --- Videotexture Main Operators
##
#class BLive_OT_videotexture_add(bpy.types.Operator):
    #'''
        #Command: Videotexture Add
        #blive.osc_videotexture_add()
    #'''
    #bl_idname = "blive.videotexture_add"
    #bl_label = "BLive add current source to playlist"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = bpy.context.object
        #image = ob.active_material.active_texture.image
        #player = image.player

        #return {'FINISHED'}

#class BLive_OT_videotexture_start(bpy.types.Operator):
    #'''
        #Command: Videotexture Start
        #blive.osc_videotexture_start()
    #'''
    #bl_idname = "blive.videotexture_start"
    #bl_label = "BLive start current source"

    #@classmethod
    #def poll(self, context):
        #try:
            #return bool(context.active_object.active_material.active_texture.image)
        #except AttributeError:
            #return False

    #def execute(self, context):
        #ob = bpy.context.object
        #image = ob.active_material.active_texture.image
        #player = image.player

        #return {'FINISHED'}

def register():
    print("texture.ops.register")
    bpy.utils.register_class(BLive_OT_videotexture_source_from_filebrowser)
    #bpy.utils.register_class(BLive_OT_videotexture_filebrowser)
    #bpy.utils.register_class(BLive_OT_videotexture_open)
    #bpy.utils.register_class(BLive_OT_videotexture_pause)
    #bpy.utils.register_class(BLive_OT_videotexture_play)
    #bpy.utils.register_class(BLive_OT_videotexture_stop)
    #bpy.utils.register_class(BLive_OT_videotexture_close)
    #bpy.utils.register_class(BLive_OT_videotexture_playlist_add)
    #bpy.utils.register_class(BLive_OT_videotexture_playlist_remove)
    #bpy.utils.register_class(BLive_OT_videotexture_add)
    #bpy.utils.register_class(BLive_OT_videotexture_start)

    bpy.utils.register_class(BLive_OT_osc_movie_open)
    #bpy.utils.register_class(BLive_OT_osc_movie_audio)
    #bpy.utils.register_class(BLive_OT_osc_movie_range)
    #bpy.utils.register_class(BLive_OT_osc_movie_loop)

    #bpy.utils.register_class(BLive_OT_osc_camera_open)

    bpy.utils.register_class(BLive_OT_osc_videotexture_close)
    bpy.utils.register_class(BLive_OT_osc_videotexture_play)
    bpy.utils.register_class(BLive_OT_osc_videotexture_pause)
    bpy.utils.register_class(BLive_OT_osc_videotexture_stop)

def unregister():
    print("texture.ops.unregister")
    #bpy.utils.unregister_class(BLive_OT_videotexture_filebrowser)
    #bpy.utils.unregister_class(BLive_OT_videotexture_open)
    #bpy.utils.unregister_class(BLive_OT_videotexture_pause)
    #bpy.utils.unregister_class(BLive_OT_videotexture_play)
    #bpy.utils.unregister_class(BLive_OT_videotexture_stop)
    #bpy.utils.unregister_class(BLive_OT_videotexture_close)
    #bpy.utils.unregister_class(BLive_OT_videotexture_playlist_add)
    #bpy.utils.unregister_class(BLive_OT_videotexture_playlist_remove)
    #bpy.utils.unregister_class(BLive_OT_videotexture_add)
    #bpy.utils.unregister_class(BLive_OT_videotexture_start)

    #bpy.utils.unregister_class(BLive_OT_osc_camera_open)

    bpy.utils.unregister_class(BLive_OT_osc_movie_open)
    #bpy.utils.unregister_class(BLive_OT_osc_movie_audio)
    #bpy.utils.unregister_class(BLive_OT_osc_movie_range)
    #bpy.utils.unregister_class(BLive_OT_osc_movie_loop)

    bpy.utils.unregister_class(BLive_OT_osc_videotexture_close)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_play)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_pause)
    bpy.utils.unregister_class(BLive_OT_osc_videotexture_stop)
    bpy.utils.unregister_class(BLive_OT_videotexture_source_from_filebrowser)
