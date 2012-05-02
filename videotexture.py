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


# --- import pyliblo
import sys
sys.path.append('/usr/lib/python3.2/site-packages')
import liblo

# --- import bge modules
from bge import texture
from bge import logic

class player:
	def __init__(self, obname, imgname):
		if not obname in logic.getCurrentScene().objects:
			raise IndexError
			
		self.__file = None
		self.__state = 'STOPPED'

		gameobject = logic.getCurrentScene().objects[obname]

		# -- Get the material that is using our texture
		if imgname:
			img = "IM{0}".format(imgname)
			matID = texture.materialID(gameobject, img)
			# -- Create the video texture
			self.video = texture.Texture(gameobject, matID)
        
	def refresh(self, boolean):
		self.video.refresh(boolean)

	@property
	def source(self):
		return self.__file
	
	@source.setter	
	def source(self, file):
		self.__file = file
		print("player.source: ", self.__file)
		# -- Load the file
		self.video.source = texture.VideoFFmpeg(self.__file)

		# -- scale the video
		self.video.source.scale = True

		# -- play the video
		self.state = 'PLAY'

	@property
	def state(self):
		return self.__state
	
	@state.setter	
	def state(self, state):
		if state == 'PLAY':
			self.video.source.play()
		elif state == 'PAUSE':
			self.video.source.pause()
		elif state == 'STOP':
			self.video.source.stop()
		self.__state = state


class camera(player):
	def __init__(self, obname, imgname):
		super().__init__(obname, imgname)
		
	@property
	def source(self):
		return self.__file
	
	@source.setter	
	def source(self, file):
		self.__file = file
		print("camera.source: ", self.__file)
		# -- Load the file
		self.video.source = bge.texture.VideoFFmpeg(self.__file, 1)

		# -- scale the video
		self.video.source.scale = True
		self.video.deinterlace = True

		# -- play
		self.state = 'PLAY'

class videotexture(object):
	TEXTURE_STATES = {'PLAY', 'PAUSE', 'STOP', 'REMOVE'}
		
	def __init__(self):
		self.textures = dict()

	def update(self):
		for i in self.textures:
			self.textures[i].refresh(True)

	def movie(self, path, args):
		obname = args[0]
		imgname = args[1]
		filename = args[2]

		if imgname in self.textures:
			del self.textures[imgname]
		try:
			print("videotexture.movie: ", obname,imgname,filename)
			self.textures[imgname] = player(obname,imgname)
			self.textures[imgname].source = filename
		except TypeError as err:
			print("err in videotexture.open: ", err)

	def camera(self, path, args):
		obname = args[0]
		imgname = args[1]
		filename = args[2]

		if imgname in self.textures:
			del self.textures[imgname]
		try:
			print("videotexture.camera: ", obname,imgname,filename)
			self.textures[imgname] = camera(obname,imgname)
			self.textures[imgname].source = filename
		except TypeError as err:
			print("err in videotexture.open: ", err)		

	def state(self, path, args):
		print("videotexture.state: ", args)
		imgname = args[0]
		state = args[1]

		if state in self.TEXTURE_STATES:
			if state == 'REMOVE':
				del self.textures[imgname]
			self.textures[imgname].state = state
