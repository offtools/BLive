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

# FIXME: max. Port number in game property is 10000

import bpy

###############################################
#
#       Network Setup Panel
#
###############################################

class BLive_PT_OscDmx_Patch(bpy.types.Panel):
    bl_label = "Osc DMX Patch"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_context = 'DRIVERS'

    #@classmethod
    #def poll(self, context):
        #pass

    def draw(self, context):
        dmx = context.scene.oscdmx

        layout = self.layout
        row = layout.row()
        row.prop(dmx, "path_prefix", text='OSC Path Prefix')
        row = layout.row()
        row.prop(dmx, "sel_method", expand=True)
        if dmx.sel_method == 'properties':
            row = layout.row()
            row.prop(dmx, "sel_type", text='Object')
            row.prop_search(dmx, "sel_item", bpy.data, dmx.sel_type, text='', icon='VIEWZOOM')
            row = layout.row()
            row.prop(dmx, "sel_dpath", text='Custom Property')
            row = layout.row()
            row.prop(dmx, "sel_chan", text='Channel')
            row = layout.row()
            row.operator('blive.oscdmx_add_channel_property', text='add')
        elif dmx.sel_method == 'script':
            row = layout.row()
            row.label("Choose a module from the Texteditor,")
            row = layout.row()
            row.label("if myscript.py exists there, insert myscript")
            row = layout.row()
            row.prop(dmx, "sel_module", text='Module')
            row = layout.row()
            row.label("add a function name from myscript,")
            row = layout.row()
            row.label("it should contain one parameter for the dmx value")
            row = layout.row()
            row.prop(dmx, "sel_function", text='Function')
            row = layout.row()
            row.prop(dmx, "sel_chan", text='Channel')
            row = layout.row()
            row.operator('blive.oscdmx_add_channel_script', text='add')

def register():
    print("oscdmx.ui.register")
    bpy.utils.register_class(BLive_PT_OscDmx_Patch)

def unregister():
    print("oscdmx.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_OscDmx_Patch)
