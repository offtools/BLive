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
from ..client import BLiveServerSingleton
from bpy.app.handlers import persistent
#~ from .ops import dmxserver

@persistent
def update_dmx_handler(scene):
	if bpy.context.window_manager.blive_settings.use_dmx_over_osc == True:
		#~ dmxserver.update()
		BLiveServerSingleton().update()

def register():
	print("oscdmx.handler.register")
	bpy.app.handlers.scene_update_post.append(update_dmx_handler)

def unregister():
	print("oscdmx.handler.unregister")

	idx = bpy.app.handlers.scene_update_post.index(update_dmx_handler)
	bpy.app.handlers.scene_update_post.remove(bpy.app.handlers.scene_update_post[idx])
