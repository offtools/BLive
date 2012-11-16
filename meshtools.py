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
import bmesh
from . import client

class BLive_OT_mesh_apply(bpy.types.Operator):
	'''
		Operator: refresh the selected mesh in the bge
	'''
	bl_idname = "blive.mesh_apply"
	bl_label = "BLive Apply Mesh Changes"
	
	def execute(self, context):
		#   send all vertex data:
		#	vertices in bge are ordered by materials and faces
		#   iterate over all faces - send each vertex of the face
		#   ob.name: object name
		#   vindex: index of the vertex inside the polygon (0 - 3)
		#   vertex.co: vertex from bmesh vertex (which is updated continuously)  
		ob = bpy.context.active_object
		try:
			mesh = bmesh.from_edit_mesh(ob.data)
			for face in mesh.faces:
				for vindex, vertex in enumerate(face.verts):
					client.client().send("/data/objects/polygon", [ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2]])
		except ValueError:
			return self.cancel(context)

		return{'FINISHED'}


class BLive_OT_modal_mesh_update(bpy.types.Operator):
	'''
		Modal Timer Operator which monitors the mesh in editmode
		and sends vertex data
	'''
	bl_idname = "blive.modal_vertex_update"
	bl_label = "BLive Vertex Updater Operator"

	_timer = None

	def modal(self, context, event):

		if event.type in {'TAB', 'ESC', 'RIGHTMOUSE'}:
			return self.cancel(context)

		if event.type == 'TIMER':
			ob = bpy.context.active_object
			try:
				mesh = bmesh.from_edit_mesh(ob.data)
				for face in mesh.faces:
					for vindex, vertex in enumerate(face.verts):
						client.client().send("/data/objects/polygon", [ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2]])
			except ValueError as err:
				print(err)
				return self.cancel(context)

		return {'PASS_THROUGH'}

	def execute(self, context):
		bpy.ops.object.mode_set(mode='EDIT')
		context.window_manager.modal_handler_add(self)
		self._timer = context.window_manager.event_timer_add(0.04, context.window)
		return {'RUNNING_MODAL'}

	def cancel(self, context):
		context.window_manager.event_timer_remove(self._timer)
		return {'FINISHED'}

#
#	BLive Mesh Tools Panel in Tool Shelf
#
class BLive_PT_mesh_tools(bpy.types.Panel):
	'''
		BLive Mesh Tools Panel in Tool Shelf
	'''
	bl_label = "BLive Mesh Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"

	@classmethod
	def poll(cls, context):
		return (context.active_object is not None) and bpy.context.active_object.mode == 'EDIT'

	def draw(self, context):
		layout = self.layout
		col = layout.column(align=True)
		col.operator("blive.mesh_apply", text="refresh remote mesh")
		col.operator("blive.modal_vertex_update", text="send mesh changes")

