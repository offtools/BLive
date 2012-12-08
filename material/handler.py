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
from ..client import BLiveClient

# TODO: Fix operator propblem in material_update_handler:36 and 44

@persistent
def material_update_handler(scene):
	color = bpy.context.window_manager.blive_settings.diffuse_to_obcolor

	if not color:
		for ob in scene.objects:
			if ob.type == 'MESH':
				# FIX: using operator here causes recursion error on startup and while animation playing
				#~ bpy.ops.blive.osc_object_obcolor(obname=ob.name)
				BLiveClient().send("/data/object/color", [ob.name, ob.color[0], ob.color[1], ob.color[2], ob.color[3]])
	else:
		if bpy.data.materials.is_updated:
			for mat in bpy.data.materials:
				if mat.is_updated:
					oblist = [ob for ob in scene.objects if ob.active_material == mat and ob.type == 'MESH']
					for ob in oblist:
						# FIX: using operator here causes recursion error on startup and while animation playing
						#~ bpy.ops.blive.osc_object_diffuse_color(obname=ob.name)
						mat = ob.active_material
						ob.color[0] = mat.diffuse_color[0]
						ob.color[1] = mat.diffuse_color[1]
						ob.color[2] = mat.diffuse_color[2]
						ob.color[3] = mat.alpha
						BLiveClient().send("/data/object/color", [ob.name, mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha])

def register():
	print("material.handler.register")
	bpy.app.handlers.scene_update_post.append(material_update_handler)

def unregister():
	print("material.handler.unregister")
	idx = bpy.app.handlers.scene_update_post.index(material_update_handler)
	bpy.app.handlers.scene_update_post.remove(bpy.app.handlers.scene_update_post[idx])
