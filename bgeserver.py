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

import bge
import types
import bgehandler
import bgevideotexture
from OSC import OSCServer

class BgeOSCServer(OSCServer):
	def __new__(type, *args):
		if not '_the_instance' in type.__dict__:
			type._the_instance = object.__new__(type)
		return type._the_instance

	def __init__(self, ip="127.0.0.1", port=9900):
		super().__init__((ip,port))
		self.timeout = 0

		# --- add videotexture module to server
		self.__module = list()
		vtex = bgevideotexture.VideoTexture()
		self._addUpdateModule(vtex)
		
		self.addMsgHandler('/connect', self.callback_connect)
		self.addMsgHandler('/debug', bgehandler.debug)
		self.addMsgHandler('/quit', bgehandler.quit)

		self.addMsgHandler("/data/object/location", bgehandler.update_object_location)
		self.addMsgHandler("/data/object/rotation", bgehandler.update_object_rotation)
		self.addMsgHandler("/data/object/scaling", bgehandler.update_object_scaling)
		self.addMsgHandler("/data/object/color", bgehandler.update_object_color)
		self.addMsgHandler("/data/object/gameproperty", bgehandler.update_object_gameproperty)

		self.addMsgHandler("/data/object/camera", bgehandler.update_camera)

		self.addMsgHandler("/data/object/lamp", bgehandler.update_lamp)
		self.addMsgHandler("/data/object/lamp/normal", bgehandler.update_lamp_normal)
		self.addMsgHandler("/data/object/lamp/spot", bgehandler.update_lamp_spot)
		self.addMsgHandler("/data/object/lamp/sun", bgehandler.update_lamp_sun)

		self.addMsgHandler("/data/object/mesh", bgehandler.update_mesh)

		self.addMsgHandler("/scene/active", bgehandler.update_active_scene)

		#
		# --- Videotexture Message handlers
		#

		# --- Videotexture - open a Movie:
		# --- object name (string)
		# --- image name (string)
		# --- filepath (string)
		# --- sound (bool)
		# --- inpoint (float)
		# --- outpoint ()
		# --- loop (bool)
		# --- preseek (int)
		# --- deinterlace (bool)
		self.addMsgHandler("/texture/movie/open", vtex.cb_movie_open)

		# --- Videotexture - set playback range:
		# --- inpoint (float)
		# --- outpoint (float)
		self.addMsgHandler("/texture/movie/range", vtex.cb_movie_range)

		# --- Videotexture - enable audio:
		# --- audio (bool)
		self.addMsgHandler("/texture/movie/audio", vtex.cb_movie_audio)

		# --- Videotexture - loop playback:
		# --- loop (bool)
		self.addMsgHandler("/texture/movie/loop", vtex.cb_movie_loop)

		# --- Videotexture - open a camera device:
		# --- object name (string)
		# --- image name (string)
		# --- filepath (string)
		# --- width (int)
		# --- height (int)
		# --- rate (float)
		# --- deinterlace (bool)
		self.addMsgHandler("/texture/camera/open", vtex.cb_camera_open)

		#
		# --- Videotexture - Status ---
		#
		# --- Videotexture - close and reset texture:
		# --- image name (string)
		self.addMsgHandler("/texture/status/close", vtex.cb_texture_close)

		# --- Videotexture - state is play:
		# --- image name (string)
		self.addMsgHandler("/texture/status/play", vtex.cb_texture_play)

		# --- Videotexture - state is pause:
		# --- image name (string)
		self.addMsgHandler("/texture/status/pause", vtex.cb_texture_pause)

		# --- Videotexture - state is stop:
		# --- image name (string)
		self.addMsgHandler("/texture/status/stop", vtex.cb_texture_stop)

		#
		# --- Filter ---
		#
		# --- Videotexture - deinterlace texture:
		# --- image name (string)
		self.addMsgHandler("/texture/filter/deinterlace", vtex.cb_filter_deinterlace)

	def handle_timeout(self):
		self.timed_out = True
		
	def _addUpdateModule(self, instance):
		if hasattr(instance, 'update'):
			if type(instance.update) in (types.FunctionType, types.MethodType):
				self.__module.append(instance)
		
	def callback_connect(self, path, tags, args, source):
		print('receiving connect: ', path, tags, args, source)
		
	def update(self):
		self.timed_out = False
		while not self.timed_out:
			self.handle_request()

		for mod in self.__module:
			mod.update()
