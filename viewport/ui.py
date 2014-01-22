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

class BLive_PT_viewport(bpy.types.Panel):
    bl_label = "BLive Viewport"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.active_object.type  == 'CAMERA'

    def draw(self, context):
        layout = self.layout

        cam = context.active_object.data

        row = layout.row()
        row.prop(cam.viewport, "active", text="use Camera as viewport")
        row = layout.row()
        row.prop(cam.viewport, "left", text="left")
        row = layout.row()
        row.prop(cam.viewport, "right", text="right")
        row = layout.row()
        row.prop(cam.viewport, "top", text="top")
        row = layout.row()
        row.prop(cam.viewport, "bottom", text="bottom")
        row = layout.row()
        row.operator("blive.osc_update_viewports", text="Stop Gameengine")

def register():
    print("viewport.ui.register")
    bpy.utils.register_class(BLive_PT_viewport)

def unregister():
    print("viewport.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_viewport)
