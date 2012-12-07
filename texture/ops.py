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
from ..client import BLiveClient

#
# --- Operators used by gui (works on active object)
# --- Wrapper for osc Operators
#
class BLive_OT_videotexture_filebrowser(bpy.types.Operator):
	bl_idname = "blive.videotexture_filebrowser"
	bl_label = "BLive open Video Filebrowser"
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
		idx = image.player.active_playlist_entry

		if image.player.has_playlist:
			bpy.ops.blive.videotexture_playlist_add(filepath=self.filepath)
		else:
			bpy.ops.blive.osc_movie_open(obname=ob.name, 
										  imgname=image.name,
										  filepath=self.filepath,
										  audio=image.player.audio,
										  loop=image.player.loop
										  )

		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

class BLive_OT_videotexture_play(bpy.types.Operator):
	'''
		sets Videotexture State to play, if used with playlist, the Operator
		checks if a playlist entry is changed and opens a new playlist entry
	'''
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
		idx = image.player.active_playlist_entry
		
		if image.player.has_playlist and image.player.playlist_entry_changed: 
			track = image.player.playlist[idx]
			bpy.ops.blive.osc_movie_open(   obname=ob.name,
											imgname=image.name,
											filepath=track.filepath,
											audio=track.audio,
											inpoint=track.inpoint,
											outpoint=track.outpoint,
											loop=track.loop,
											preseek=track.preseek,
											deinterlace=track.deinterlace  )
			image.player.playlist_entry_changed=False
		else:
			bpy.ops.blive.osc_videotexture_play(imgname=image.name)

		image.player.playlist_entry_changed=False
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
		bpy.ops.blive.osc_videotexture_pause(imgname=image.name)
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
		bpy.ops.blive.osc_videotexture_stop(imgname=image.name)
		player.playlist_entry_changed = True
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
		ob = bpy.context.object
		image = ob.active_material.active_texture.image
		player = image.player
		bpy.ops.blive.osc_videotexture_close(imgname=image.name)
		player.playlist_entry_changed = True
		return {'FINISHED'}

class BLive_OT_videotexture_playlist_add(bpy.types.Operator):
	bl_idname = "blive.videotexture_playlist_add"
	bl_label = "BLive add Playlist Entry"
	filepath = bpy.props.StringProperty()

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
		
		track = image.player.playlist.add()
		track.name = os.path.basename(self.filepath)
		track.filepath = self.filepath
		player.active_playlist_entry = len(player.playlist)-1

		return {'FINISHED'}

#
# --- Client OSC Operators
#

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
		BLiveClient().send("/texture/movie/open", [ 
							self.obname, 
							self.imgname, 
							self.filepath, 
							int(self.audio), 
							self.inpoint, 
							self.outpoint, 
							int(self.loop), 
							self.preseek, 
							int(self.deinterlace) ]
							)

		return {'FINISHED'}

class BLive_OT_osc_movie_audio(bpy.types.Operator):
	'''
		OSC Command: enable audio for Videotexture
		bpy.ops.blive.osc_movie_audion(imgname='image')
	'''
	bl_idname = "blive.osc_movie_audio"
	bl_label = "BLive enable Audio for Videotexture"

	imgname = bpy.props.StringProperty()
	audio = bpy.props.BoolProperty(default=False)

	def execute(self, context):
		BLiveClient().send("/texture/movie/audio", [ 
							self.imgname, 
							self.audio ]
							)
		return {'FINISHED'}

class BLive_OT_osc_movie_range(bpy.types.Operator):
	'''
		OSC Command: set in and outpoints for moviefile
		bpy.ops.blive.osc_movie_range(imgname='image')
	'''
	bl_idname = "blive.osc_movie_range"
	bl_label = "BLive Set Movie In- and Outpoints"
	
	imgname = bpy.props.StringProperty()
	inp = bpy.props.FloatProperty(default=0.0)
	outp = bpy.props.FloatProperty(default=0.0)

	def execute(self, context):
		BLiveClient().send("/texture/movie/audio", [ 
							self.imgname, 
							self.inp, self.outp ]
							)
		return {'FINISHED'}

class BLive_OT_osc_movie_loop(bpy.types.Operator):
	'''
		OSC Command: loop videotexture movie playback 
		bpy.ops.blive.osc_movie_loop(imgname='image')
	'''
	bl_idname = "blive.osc_movie_loop"
	bl_label = "BLive Loop Movie"
	
	imgname = bpy.props.StringProperty()
	loop = bpy.props.BoolProperty(default=False)

	def execute(self, context):
		BLiveClient().send("/texture/movie/loop", [ 
							self.imgname, 
							int(self.loop) ]
							)
		return {'FINISHED'}

#
# --- Videotexture Status Operators 
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
		BLiveClient().send("/texture/status/close", [self.imgname])
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
		BLiveClient().send("/texture/status/play", [self.imgname])
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
		BLiveClient().send("/texture/status/pause", [self.imgname])
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
		BLiveClient().send("/texture/status/stop", [self.imgname])
		return {'FINISHED'}

#
# --- Videotexture Filter Operators
#
class BLive_OT_osc_filter_deinterlace(bpy.types.Operator):
	'''
		OSC Command: Videotexture Stop 
		blive.osc_videotexture_play(imgname='image', deinterlace='False')
	'''
	bl_idname = "blive.osc_videotexture_filter"
	bl_label = "BLive Deinterlace Videotexture"
	
	imgname = bpy.props.StringProperty()
	deinterlace = bpy.props.BoolProperty(default=False)
	
	def execute(self, context):
		BLiveClient().send("/texture/filter/deinterlace", [
							self.imgname,
							self.deinterlace ]
							)
		return {'FINISHED'}

def register():
	print("texture.ops.register")
	bpy.utils.register_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.register_class(BLive_OT_videotexture_pause)
	bpy.utils.register_class(BLive_OT_videotexture_play)
	bpy.utils.register_class(BLive_OT_videotexture_stop)
	bpy.utils.register_class(BLive_OT_videotexture_close)
	bpy.utils.register_class(BLive_OT_videotexture_playlist_add)

	bpy.utils.register_class(BLive_OT_osc_movie_open)
	bpy.utils.register_class(BLive_OT_osc_movie_audio)
	bpy.utils.register_class(BLive_OT_osc_movie_range)
	bpy.utils.register_class(BLive_OT_osc_movie_loop)
	
	bpy.utils.register_class(BLive_OT_osc_videotexture_close)
	bpy.utils.register_class(BLive_OT_osc_videotexture_play)
	bpy.utils.register_class(BLive_OT_osc_videotexture_pause)
	bpy.utils.register_class(BLive_OT_osc_videotexture_stop)

def unregister():
	print("texture.ops.unregister")
	bpy.utils.unregister_class(BLive_OT_videotexture_filebrowser)
	bpy.utils.unregister_class(BLive_OT_videotexture_pause)
	bpy.utils.unregister_class(BLive_OT_videotexture_play)
	bpy.utils.unregister_class(BLive_OT_videotexture_stop)
	bpy.utils.unregister_class(BLive_OT_videotexture_close)
	bpy.utils.unregister_class(BLive_OT_videotexture_playlist_add)
	
	bpy.utils.unregister_class(BLive_OT_osc_movie_open)
	bpy.utils.unregister_class(BLive_OT_osc_movie_audio)
	bpy.utils.unregister_class(BLive_OT_osc_movie_range)
	bpy.utils.unregister_class(BLive_OT_osc_movie_loop)
	
	bpy.utils.unregister_class(BLive_OT_osc_videotexture_close)
	bpy.utils.unregister_class(BLive_OT_osc_videotexture_play)
	bpy.utils.unregister_class(BLive_OT_osc_videotexture_pause)
	bpy.utils.unregister_class(BLive_OT_osc_videotexture_stop)
