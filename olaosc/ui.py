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

class BLive_PT_olaosc_patch(bpy.types.Panel):
	bl_label = "BLive - OLA OSC"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"

	@classmethod
	def poll(self, context):
		return context.window_manager.blive_settings.use_olaosc

	def draw_action_properties(self, box, target, action):
		row = box.row()
		row.prop_search(action, "attr", target.bl_rna, "properties", text='Attribute', icon='VIEWZOOM')
		if not action.attr:
			return
		if isinstance(target.bl_rna.properties[action.attr], bpy.types.BoolProperty):
			row = box.row()
			row.prop(action, "channel")
		elif isinstance(target.bl_rna.properties[action.attr], bpy.types.FloatProperty):
			row = box.row()
			length = target.bl_rna.properties[action.attr].array_length
			if length:
				row.prop(action, "attr_idx")
			row.prop(action, "precision")
			row = box.row()
			row.prop(action, "min")
			row.prop(action, "max")
			row = box.row()
			row.prop(action, "channel")
		elif isinstance(target.bl_rna.properties[action.attr], bpy.types.IntProperty):
			row = box.row()
			length = target.bl_rna.properties[action.attr].array_length
			if length:
				row.prop(action, "attr_idx")
			row = box.row()
			row.prop(action, "min")
			row.prop(action, "max")
			row = box.row()
			row.prop(action, "channel")
		else:
			row = box.row()
			row.label("unable to patch this value")

	def draw(self, context):
		layout = self.layout
		bs = context.window_manager.blive_settings
		olaosc = context.scene.olaosc

		# --- box network
		box = layout.box()
		row = box.row()
		row.label("Network Setup")
		row = box.row()
		row.prop(bs, "olaosc_server", text="Server")
		row = box.row()
		row.prop(bs, "olaosc_port", text="Port")

		row = box.row()
		row.operator("blive.olaosc_enable", text="connect")
		row.operator("blive.olaosc_disable", text="disconnect")

		row = box.row(align=True)
		if not olaosc.universes:
			row.operator("blive.olaosc_add_universe", text='add Universe')
			return

		# --- box universe
		box = layout.box()
		row = box.row()
		row.label("OLA Universes")
		row = box.row()
		split = row.split(percentage=0.9)
		split.template_list(olaosc, "universes", olaosc, "active_universe", rows=2, maxrows=8)

		col = split.column(align=True)
		col.operator("blive.olaosc_add_universe", text='', icon='ZOOMIN')
		col.operator("blive.olaosc_del_universe", text='', icon='ZOOMOUT')
		row = box.row()
		row.prop(olaosc.universes[olaosc.active_universe], "name", text="name")
		row = box.row()
		row.prop(olaosc.universes[olaosc.active_universe], "oscpath", text="osc path")

		universe = olaosc.universes[olaosc.active_universe]

		# --- box actions
		box = layout.box()
		row = box.row()
		if not universe.actions:
			row = box.row()
			row.label("Add Action and assign a Channel")
			row = box.row()
			row.operator("blive.olaosc_add_action", text='add')
			return
		row.label("Actions")
		row = box.row()
		split = row.split(percentage=0.9)
		split.template_list(universe, "actions", universe, "active_action", rows=2, maxrows=8)

		col = split.column(align=True)
		col.operator("blive.olaosc_add_action", text='', icon='ZOOMIN')
		col.operator("blive.olaosc_del_action", text='', icon='ZOOMOUT')

		# --- box action properties
		box = layout.box()
		row = box.row()
		row.label("Patch Actions")
		row = box.row()
		row. prop(universe, 'context', icon='ZOOMIN', expand=True, icon_only=True, index=-1)
		
		action = universe.actions[universe.active_action]

		row = box.row()
		# --- Object, Textures, Materials
		if universe.context == 'ctx_object':
			row.prop_search(action, "target", context.scene, "objects", text='Object', icon='OBJECT_DATA')
			if action.target:
				target = context.scene.objects[action.target]
				if action and target:
					self.draw_action_properties(box, target, action)
		elif universe.context == 'ctx_material':
			row.prop_search(action, "target", bpy.data, "materials", text='Object', icon='MATERIAL')
			if action.target:
				target = bpy.data.materials[action.target]
				if action and target:
					self.draw_action_properties(box, target, action)
		elif universe.context == 'ctx_texture':
			row.prop_search(action, "target", bpy.data, "textures", text='Object', icon='MATERIAL')
			if action.target:
				target = bpy.data.textures[action.target]
				if action and target:
					self.draw_action_properties(box, target, action)
		# --- Operator
		elif universe.context == 'ctx_operator':
			row.prop(action, "target", text="Operator")
			if action.target:
				try:
					op = eval("bpy.ops.%s"%action.target)
					target = op.get_rna()
					if action and target:
						self.draw_action_properties(box, target, action)
				except (KeyError, AttributeError, SyntaxError) as err:
					row = box.row()
					row.label("Error: Operator not found")

def register():
	print("olaosc.ui.register")
	bpy.utils.register_class(BLive_PT_olaosc_patch)

def unregister():
	print("olaosc.ui.unregister")
	bpy.utils.unregister_class(BLive_PT_olaosc_patch)
