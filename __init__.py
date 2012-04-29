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
# Blender OSC-BGE addon, this addon allows to send changes from blender 
# to a running gameengine instance
#

bl_info = {
	"name": "BLive",
	"author": "offtools",
	"version": (0, 0, 1),
	"blender": (2, 6, 0),
	"location": "View3D > Spacebar Key",
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
else:
	from . import logic
	from . import client
	from . import timeline
	from . import texture
	   
import bpy
import bmesh
import sys
import subprocess
sys.path.append('/usr/lib/python3.2/site-packages')
import liblo

#
#	Scene Network Panel
#
class BLive_PT_scene_network(bpy.types.Panel):
	bl_label = "BLive Network"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def draw(self, context):
		self.layout.label(text="Setup")

		box = self.layout.box()
		box.label("add OSC logic to: {}".format(bpy.context.scene.camera.name))

		row = box.row(align=True)
		if "PORT" in bpy.context.scene.camera.game.properties:
			row.label("Port: ")
			row.prop(bpy.context.scene.camera.game.properties["PORT"], "value", text='')
			row.operator("blive.logic_remove", text="", icon="CANCEL")
		else:
			row.operator("blive.logic_add", text="create scripts")
		row = self.layout.row()
		row.operator_context = 'INVOKE_AREA'
		row.operator("wm.save_as_mainfile", text="Save As...")
		row = self.layout.row()
		row.operator("blive.fork_blenderplayer", text="Start")
		if "PORT" not in bpy.context.scene.camera.game.properties or not bpy.context.blend_data.filepath:
			row.enabled = False 
		row = self.layout.row()
		row.operator("blive.quit", text="Quit")

class BLive_OT_forc_blenderplayer(bpy.types.Operator):
	bl_idname = "blive.fork_blenderplayer"
	bl_label = "BLive fork blenderplayer"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			app = "blenderplayer"
			blendfile = bpy.context.blend_data.filepath
			port = "-p {0}".format(bpy.context.scene.camera.game.properties["PORT"].value)
			cmd = [app,  port, blendfile]
			blendprocess = subprocess.Popen(cmd)
			bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler)
			bpy.app.handlers.scene_update_post.append(scene_update_post_handler)
			return{'FINISHED'}
		else:
			return{'CANCELLED'}

class BLive_OT_quit(bpy.types.Operator):
	bl_idname = "blive.quit"
	bl_label = "BLive quit blenderplayer"

	def execute(self, context):
		if "PORT" in bpy.context.scene.camera.game.properties:
			client.client().quit()
			# TODO unregister app handlers
			for i in bpy.app.handlers.frame_change_post:
				bpy.app.handlers.frame_change_post.remove(i)
			for i in bpy.app.handlers.scene_update_post:
				bpy.app.handlers.scene_update_post.remove(i)
			return{'FINISHED'}
		else:
			return{'CANCELLED'}

def scene_update_post_handler(scene):

	if bpy.data.objects.is_updated:
		for ob in bpy.data.objects:
			if ob.is_updated:
				client.client().snd_object(ob)

class BLive_OT_mesh_apply(bpy.types.Operator):
	bl_idname = "blive.mesh_apply"
	bl_label = "BLive Apply Mesh Changes"
	
	def execute(self, context):
		#   send all vertex data
		#   iterate over all faces - send each vertex of the polygons
		#   ob.name: object name
		#   vindex: index of the vertex inside the polygon (0 - 3)
		#   vertex.co: vertex from bmesh vertex (which is updated continuously)  
		ob = bpy.context.active_object
		try:
			mesh = bmesh.from_edit_mesh(ob.data)
			for face in mesh.faces:
				for vindex, vertex in enumerate(face.verts):
					client.client().send("/data/objects/polygon", ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2])
		except ValueError:

		return{'FINISHED'}

class BLive_OT_modal_mesh_update(bpy.types.Operator):
	'''Operator which runs its self from a timer.'''
	bl_idname = "blive.modal_vertex_update"
	bl_label = "BLive Vertex Updater Operator"

	_timer = None

	def modal(self, context, event):

		if event.type in {'LEFTMOUSE', 'TAB', 'ESC', 'RIGHTMOUSE'}:
			return self.cancel(context)

		if event.type == 'TIMER':
			ob = bpy.context.active_object
			try:
				mesh = bmesh.from_edit_mesh(ob.data)
				for face in mesh.faces:
					for vindex, vertex in enumerate(face.verts):
						client.client().send("/data/objects/polygon", ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2])
			except ValueError:
				return self.cancel(context)

		return {'PASS_THROUGH'}

	def execute(self, context):
		bpy.ops.object.mode_set(mode='EDIT')
		context.window_manager.modal_handler_add(self)
		self._timer = context.window_manager.event_timer_add(0.1, context.window)
		return {'RUNNING_MODAL'}

	def cancel(self, context):
		context.window_manager.event_timer_remove(self._timer)
		return {'FINISHED'}

class BLive_PT_mesh_tools(bpy.types.Panel):
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

def frame_change_pre_handler(scene):
	# stop animation
	if not bpy.context.active_object.mode == 'OBJECT':
		if bpy.context.screen.is_animation_playing:
			bpy.ops.screen.animation_play()

	cur = scene.frame_current
	marker = [ (i.frame, i) for i in scene.timeline_markers if i.frame >= cur]
	if len(marker):
		nextmarker = min(marker)[1]
		# animation is passing a marker
		if nextmarker.frame == cur:
			# check if we have an event queue with the same name as the current marker
			if nextmarker.name in bpy.context.scene.timeline_queues:
				# check pause
				if scene.timeline_queues[nextmarker.name].m_pause and bpy.context.screen.is_animation_playing:
					bpy.ops.screen.animation_play()
				# send events
				for item in scene.timeline_queues[nextmarker.name].m_items:
					item.trigger()

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
	print("registering blive modules")
	register()
