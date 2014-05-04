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
from ..common.libloclient import Client

###############################################
#
#       Network Setup Panel
#
###############################################

class BLive_PT_OscDmx_Patch(bpy.types.Panel):
    bl_label = "Osc DMX Patch"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    #@classmethod
    #def poll(self, context):
        #pass

    def draw(self, context):
        dmx = context.scene.oscdmx

        layout = self.layout
        box = layout.box()
        box.label("OSC Port for qlcplus: {0}".format(Client().port))
        row = box.row()
        row.prop(dmx, "path_prefix", text='OSC Prefix')
        row = box.row()
        if bpy.app.version[1] < 66:
            row.template_list(dmx, "channels", dmx, "active_channel", rows=2, maxrows=4)
        else:
            row.template_list("UI_UL_list", "channels", dmx, "channels", dmx, "active_channel", rows=2, maxrows=4)
        row = box.row()
        row.prop(dmx, "active_channel_by_name", text='Channel')
        row.operator('blive.oscdmx_add_channel', text='', icon='ZOOMIN')

        if str(dmx.active_channel_by_name) in dmx.channels:
            row = box.row()
            row.prop(dmx, "sel_method", expand=True)
            channel = dmx.channels[dmx.active_channel]

            if dmx.sel_method == 'properties':
                row = box.row()
                if bpy.app.version[1] < 66:
                    row.template_list(channel, "properties", dmx, "active_prop_handler", rows=2, maxrows=8)
                else:
                    row.template_list("UI_UL_list", "properties", channel, "properties", dmx, "active_prop_handler", rows=2, maxrows=8)
                col = row.column(align=True)
                col.operator('blive.oscdmx_add_channel_handler', text='', icon='ZOOMIN')
                col.operator('blive.oscdmx_del_channel_handler', text='', icon='ZOOMOUT')

                if len(channel.properties) > dmx.active_prop_handler:
                    handler = channel.properties[dmx.active_prop_handler]

                    row = box.row(align=True)
                    row.prop(handler, "type_enum", text='ID Data')
                    row.prop_search(handler, "id_data", bpy.data, handler.type_enum, text='', icon='VIEWZOOM')
                    row = box.row()
                    row.prop(handler, "data_path", text='Property')
                    if handler.index > -1:
                        row = box.row()
                        row.prop(handler, "index", text='Index')
                    row = box.row()
                    row.prop(handler, "min", text='min')
                    row = box.row()
                    row.prop(handler, "max", text='max')


            elif dmx.sel_method == 'script':
                row = box.row()
                if bpy.app.version[1] < 66:
                    row.template_list(channel, "scripts", dmx, "active_script_handler", rows=2, maxrows=8)
                else:
                    row.template_list("UI_UL_list", "scripts", channel, "scripts", dmx, "active_script_handler", rows=2, maxrows=8)
                col = row.column(align=True)
                col.operator('blive.oscdmx_add_channel_handler', text='', icon='ZOOMIN')
                col.operator('blive.oscdmx_del_channel_handler', text='', icon='ZOOMOUT')

                if len(channel.scripts) > dmx.active_script_handler:
                    handler = channel.scripts[dmx.active_script_handler]

                    row = box.row()
                    row.prop_search(handler, "module", bpy.data, 'texts', text='Script', icon='VIEWZOOM')
                    if not handler.module[-3:] == '.py':
                        row = box.row()
                        row.label('(script name should contain .py suffix!)')
                    else:
                        row = box.row()
                        row.prop(handler, "function", text='Function')


def register():
    print("oscdmx.ui.register")
    bpy.utils.register_class(BLive_PT_OscDmx_Patch)

def unregister():
    print("oscdmx.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_OscDmx_Patch)
