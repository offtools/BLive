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

# TODO: add basic blive_init on every startup (only path append and import statement)

import bpy
import re
from ..common.libloclient import Client

def dmx_callback(path, args, types, source, user_data):
    context = bpy.context
    oscdmx = context.scene.oscdmx
    chan = oscdmx.channels[str(user_data)]
    for p in chan:
        p.execute(args[0])

class BLive_OT_OscDmx_register_channels(bpy.types.Operator):
    '''OSC dmx - register channels, done by client connect'''
    bl_idname = "blive.oscdmx_register_channels"
    bl_label = "OscDmx register channels"

    def execute(self, context):
        oscdmx = context.scene.oscdmx
        for ch in oscdmx.channels:
            Client().add_method("{0}/{1}".format(oscdmx.path_prefix, int(ch.name)), "f", dmx_callback, int(ch.name))
            ch.registered = True
        return{'FINISHED'}

class BLive_OT_OscDmx_add_channel_property(bpy.types.Operator):
    '''OSC dmx - add property to channel'''
    bl_idname = "blive.oscdmx_add_channel_property"
    bl_label = "OscDmx add channel property"

    #@classmethod
    #def poll(self, context):
        #return not len(context.scene.oscdmx.universe)

    def execute(self, context):
        oscdmx = context.scene.oscdmx
        if not str(oscdmx.sel_chan) in oscdmx.channels:
            ch = oscdmx.channels.add()
            ch.name = str(oscdmx.sel_chan)
            Client().add_method("{0}/{1}".format(oscdmx.path_prefix, oscdmx.sel_chan), "f", dmx_callback, oscdmx.sel_chan)
            ch.registered = True

        prop = oscdmx.channels[str(oscdmx.sel_chan)].properties.add()
        prop.type_enum = oscdmx.sel_type
        prop.id_data = oscdmx.sel_item
        if hasattr(oscdmx.sel_dpath, '__len__') and '[' in oscdmx.sel_dpath:
            pattern=re.compile(r"[\[\]]")
            sp = pattern.split(oscdmx.sel_dpath)
            prop.data_path = sp[0]
            prop.index = int(sp[1])
        else:
            prop.data_path = oscdmx.sel_dpath
        return{'FINISHED'}

class BLive_OT_OscDmx_add_channel_script(bpy.types.Operator):
    '''OSC dmx - add script to channel'''
    bl_idname = "blive.oscdmx_add_channel_script"
    bl_label = "OscDmx add channel script"

    #@classmethod
    #def poll(self, context):
        #return not len(context.scene.oscdmx.universe)

    def execute(self, context):
        oscdmx = context.scene.oscdmx
        if not str(oscdmx.sel_chan) in oscdmx.channels:
            ch = oscdmx.channels.add()
            ch.name = str(oscdmx.sel_chan)
            Client().add_method("{0}/{1}".format(oscdmx.path_prefix, oscdmx.sel_chan), "f", dmx_callback, oscdmx.sel_chan)
            ch.registered = True

        script = oscdmx.channels[str(oscdmx.sel_chan)].script.add()
        script.module = oscdmx.sel_module
        script.function = oscdmx.sel_function
        return{'FINISHED'}

def register():
    print("oscdmx.ops.register")
    bpy.utils.register_class(BLive_OT_OscDmx_add_channel_property)
    bpy.utils.register_class(BLive_OT_OscDmx_add_channel_script)
    bpy.utils.register_class(BLive_OT_OscDmx_register_channels)

def unregister():
    print("oscdmx.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_OscDmx_register_channels)
    bpy.utils.register_class(BLive_OT_OscDmx_add_channel_script)
    bpy.utils.unregister_class(BLive_OT_OscDmx_add_channel_property)
