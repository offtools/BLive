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
		gameobject = logic.getCurrentScene().objects[obname]

		# -- Get the material that is using our texture
		if imgname:
			img = "IM{0}".format(imgname)
			matID = texture.materialID(gameobject, img)
			# -- Create the video texture
			self.video = texture.Texture(gameobject, matID)
        
	def refresh(self, boolean):
		self.video.refresh(boolean)

	def __setsource(self, file):
		self.__file = file

		# -- Load the file
		self.video.source = texture.VideoFFmpeg(self.__file)

		# -- scale the video
		self.video.source.scale = True

		# -- play the video
		self.video.source.play()


		src = self.video.source

	def __getsource(self):
		return self.__file

	source = property(__getsource, __setsource)

class camera(player):
	def __init__(self, obname, imgname):
		super(camera, self).__init__(obname, imgname)
		
	def __setsource(self, file):
		self.__file = file

		# -- Load the file
		self.video.source = bge.texture.VideoFFmpeg("/dev/video0", 0, 0, 64, 48)

		# -- scale the video
		self.video.source.scale = False
		self.video.source.deinterlace = True
		
		# -- play the video
		self.video.source.play()
		print("camera valid: ", self.video.source.valid)

class videotexture(object):

	def __init__(self):
		self.players = dict()

	def update(self):
		for i in self.players:
			self.players[i].refresh(True)
		
	def movie(self, path, args):
		obname = args[0]
		imgname = args[1]
		filename = args[2]

		if imgname in self.players:
			del self.players[imgname]
		try:
			print("videotexture.movie: ", obname,imgname,filename)
			self.players[imgname] = player(obname,imgname)
			self.players[imgname].source = filename
		except TypeError as err:
			print("err in videotexture.open: ", err)

	def camera(self, path, args):
		obname = args[0]
		imgname = args[1]
		filename = args[2]

		if imgname in self.players:
			del self.players[imgname]
		try:
			print("videotexture.camera: ", obname,imgname,filename)
			self.players[imgname] = camera(obname,imgname)
			self.players[imgname].source = filename
		except TypeError as err:
			print("err in videotexture.open: ", err)		

	def state(self, path, args):
		print("videotexture.state: ", args)
