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


#
#	Blender OSC-BGE addon, this addon allows to send changes from blender 
#	to a running gameengine instance
#
#	1. install pyliblo
#	2. check search path for liblo in client.py and server.py
#	3. enable the blive addon
#	4. setup BLive in the Properties->Scene->Blive Network Panel
#

bl_info = {
	"name": "BLive",
	"author": "offtools",
	"version": (0, 0, 1),
	"blender": (2, 6, 4),
	"location": "various Panels with prefix BLive",
	"description": "blender to bge osc network addon",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Game Engine"}
	
# import modules
if "bpy" in locals():
	import imp
	imp.reload('logic')
	imp.reload('client')
	imp.reload('timeline')
	imp.reload('texture')
#	imp.reload('meshtools')
	imp.reload('apphandler')
	imp.reload('properties')
	imp.reload('network')
else:
	from . import logic
	from . import client
	from . import timeline
	from . import marker
	from . import texture
#	from . import meshtools
	from . import apphandler
	from . import properties
	from . import network

import bpy

def register():
	print("__init__.register")
	properties.register()
	bpy.utils.register_module(__name__)
	apphandler.register()

def unregister():
	print("__init__.unregister")
	apphandler.unregister()
	properties.unregister()
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	pass
