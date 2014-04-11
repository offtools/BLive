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

#TODO: make popup operators for adding new handlers (reduce doubles properties in props)

import bpy
import re
from .props import type_enum
from ..common.libloclient import Client
from ..utils.utils import unique_name

def dmx_callback(path, args, types, source, user_data):
    context = bpy.context
    oscdmx = context.scene.oscdmx
    chan = oscdmx.channels[str(user_data)]
    for p in chan:
        p.execute(chan, args[0])

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
    bl_options = {'REGISTER', 'UNDO'}

    channel = bpy.props.IntProperty(default=0, min=0, max=254)
    type_enum = bpy.props.EnumProperty(name='ID Type', items=type_enum)
    id_data = bpy.props.StringProperty()
    data_path = bpy.props.StringProperty()
    index = bpy.props.IntProperty(default=-1)
    min = bpy.props.FloatProperty(default=0.0)
    max = bpy.props.FloatProperty(default=1.0)


    #@classmethod
    #def poll(self, context):
        #return not len(context.scene.oscdmx.universe)

    def execute(self, context):
        self.report({'INFO'}, 'EXECUTE')
        oscdmx = context.scene.oscdmx
        if not str(oscdmx.sel_chan) in oscdmx.channels:
            ch = oscdmx.channels.add()
            ch.name = str(oscdmx.sel_chan)
            Client().add_method("{0}/{1}".format(oscdmx.path_prefix, oscdmx.sel_chan), "f", dmx_callback, oscdmx.sel_chan)
            ch.registered = True

        channel = oscdmx.channels[str(oscdmx.sel_chan)]
        prop = channel.properties.add()
        prop.name = unique_name(channel.properties, 'prop')
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

class BLive_OT_OscDmx_delete_channel_property(bpy.types.Operator):
    '''OSC dmx - delete channel property handler'''
    bl_idname = "blive.oscdmx_delete_channel_property"
    bl_label = "OscDmx delete channel property handler"

    def execute(self, context):
        dmx = context.scene.oscdmx
        dmx.channels[dmx.sel_search_channel].properties.remove(dmx.sel_prop_idx)
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

        channel = oscdmx.channels[str(oscdmx.sel_chan)]
        script = channel.scripts.add()
        script.name = unique_name(channel.properties, 'script')
        if oscdmx.sel_module[-3:] == '.py':
            script.module = oscdmx.sel_module[:-3]
        else:
            script.module = oscdmx.sel_module
        script.function = oscdmx.sel_function
        return{'FINISHED'}

class BLive_OT_OscDmx_delete_channel_script(bpy.types.Operator):
    '''OSC dmx - delete channel script handler'''
    bl_idname = "blive.oscdmx_delete_channel_script"
    bl_label = "OscDmx delete channel script handler"

    def execute(self, context):
        dmx = context.scene.oscdmx
        dmx.channels[dmx.sel_search_channel].scripts.remove(dmx.sel_script_idx)
        return{'FINISHED'}

class BLive_OT_OscDmx_add_channel(bpy.types.Operator):
    '''OSC dmx - add dmx channel'''
    bl_idname = "blive.oscdmx_add_channel"
    bl_label = "OscDmx add channel"

    def execute(self, context):
        dmx = context.scene.oscdmx
        if not str(dmx.active_channel_by_name) in dmx.channels:
            ch = dmx.channels.add()
            dmx.active_channel = len(dmx.channels) - 1
            ch.name = str(dmx.active_channel_by_name)
            Client().add_method("{0}/{1}".format(dmx.path_prefix, dmx.active_channel_by_name), "f", dmx_callback, dmx.active_channel_by_name)
            ch.registered = True
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_OscDmx_add_channel_handler(bpy.types.Operator):
    '''OSC dmx - add channel handler'''
    bl_idname = "blive.oscdmx_add_channel_handler"
    bl_label = "OscDmx add channel handler"

    @classmethod
    def poll(self, context):
        return bool(str(context.scene.oscdmx.active_channel_by_name) in context.scene.oscdmx.channels)

    def execute(self, context):
        dmx = context.scene.oscdmx
        channel = dmx.channels[dmx.active_channel]
        if dmx.sel_method == 'properties':
            prop = channel.properties.add()
            prop.name = unique_name(channel.properties, 'prop')
        elif dmx.sel_method == 'script':
            script = channel.scripts.add()
            script.name = unique_name(channel.scripts, 'script')
        return{'FINISHED'}

class BLive_OT_OscDmx_del_channel_handler(bpy.types.Operator):
    '''OSC dmx - del channel handler'''
    bl_idname = "blive.oscdmx_del_channel_handler"
    bl_label = "OscDmx del channel handler"

    @classmethod
    def poll(self, context):
        return bool(str(context.scene.oscdmx.active_channel_by_name) in context.scene.oscdmx.channels)

    def execute(self, context):
        dmx = context.scene.oscdmx
        channel = dmx.channels[dmx.active_channel]
        if dmx.sel_method == 'properties':
            dmx.channels[dmx.active_channel].properties.remove(dmx.active_prop_handler)
        elif dmx.sel_method == 'script':
            dmx.channels[dmx.active_channel].scripts.remove(dmx.active_script_handler)
        return{'FINISHED'}

def register():
    print("oscdmx.ops.register")
    #bpy.utils.register_class(BLive_OT_OscDmx_add_channel_property)
    #bpy.utils.register_class(BLive_OT_OscDmx_delete_channel_property)
    #bpy.utils.register_class(BLive_OT_OscDmx_add_channel_script)
    #bpy.utils.register_class(BLive_OT_OscDmx_delete_channel_script)
    #bpy.utils.register_class(BLive_OT_OscDmx_register_channels)

    bpy.utils.register_class(BLive_OT_OscDmx_add_channel)
    bpy.utils.register_class(BLive_OT_OscDmx_add_channel_handler)
    bpy.utils.register_class(BLive_OT_OscDmx_del_channel_handler)

def unregister():
    print("oscdmx.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_OscDmx_del_channel_handler)
    bpy.utils.unregister_class(BLive_OT_OscDmx_add_channel_handler)
    bpy.utils.unregister_class(BLive_OT_OscDmx_add_channel)

    #bpy.utils.unregister_class(BLive_OT_OscDmx_register_channels)
    #bpy.utils.unregister_class(BLive_OT_OscDmx_delete_channel_script)
    #bpy.utils.register_class(BLive_OT_OscDmx_add_channel_script)
    #bpy.utils.unregister_class(BLive_OT_OscDmx_delete_channel_property)
    #bpy.utils.unregister_class(BLive_OT_OscDmx_add_channel_property)
