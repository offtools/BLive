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

class BLive_PT_network_setup(bpy.types.Panel):
    bl_label = "BLive Network Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    #@classmethod
    #def poll(self, context):
        #pass

    def draw(self, context):
        layout = self.layout
        bs = context.window_manager.blive_settings
        server = bs.server
        port = bs.server

        row = layout.row()

        flow = row.column_flow(columns=2, align=False)
        flow.label("Server:")
        flow.label("Port:")
        flow.prop(bs, "server", text="")
        flow.prop(bs, "port", text="")

        row = layout.row()
        row.label("Start Gameengine and connect")
        row = layout.row()
        row.operator("blive.gameengine_start", text="Start Gameengine")
        row = layout.row()
        row.operator("blive.gameengine_reload", text="Reload Gameengine")
        row = layout.row()
        row.operator("blive.gameengine_stop", text="Stop Gameengine")

class BLive_PT_debug(bpy.types.Panel):
    bl_label = "BLive Debug"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    #TODO: test if connect
    #@classmethod
    #def poll(self, context):
        #pass

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.window_manager.blive_debug, "message", text="msg")
        row = layout.row()
        row.operator("blive.osc_send_message", text="send")

def register():
    print("settings.ui.register")
    bpy.utils.register_class(BLive_PT_network_setup)
    bpy.utils.register_class(BLive_PT_debug)

def unregister():
    print("settings.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_network_setup)
    bpy.utils.unregister_class(BLive_PT_debug)
