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
from bpy.app.handlers import persistent
from . import ops 

@persistent
def object_update_handler(scene):
	# --- check objects updates
	for ob in scene.objects:
		if ob.is_updated:
			#~ bpy.ops.blive.osc_object_location(obname=ob.name)
			#~ bpy.ops.blive.osc_object_rotation(obname=ob.name)
			ops.osc_object_location(ob)
			ops.osc_object_rotation(ob)

			if ob.type == 'MESH':
				#~ bpy.ops.blive.osc_object_scaling(obname=ob.name)
				ops.osc_object_scaling(ob)

			if ob.type == 'CAMERA':
				#~ bpy.ops.blive.osc_object_camera(obname=ob.name)
				ops.osc_object_camera(ob)

			if ob.type == 'LAMP':
				#~ bpy.ops.blive.osc_object_lamp(obname=ob.name)
				ops.osc_object_lamp(ob)

	# --- check mesh update
	for ob in scene.objects:
		if ob.is_updated_data and ob.type == 'MESH' and ob.mode == 'EDIT':
			#~ bpy.ops.blive.osc_object_meshdata(obname=ob.name)
			ops.osc_object_meshdata(ob)

def register():
	print("object.handler.register")
	bpy.app.handlers.scene_update_post.append(object_update_handler)

def unregister():
	print("object.handler.unregister")
	idx = bpy.app.handlers.scene_update_post.index(object_update_handler)
	bpy.app.handlers.scene_update_post.remove(bpy.app.handlers.scene_update_post[idx])
