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
from .libloclient import Client

class BLiveSettings(bpy.types.PropertyGroup):
    """blender wide Settings
    """
    port = bpy.props.IntProperty(default=9900, min=9000, max=90000)
    server = bpy.props.StringProperty(default="127.0.0.1")
    bge_window_width = bpy.props.IntProperty(default=640)
    bge_window_height = bpy.props.IntProperty(default=480)
    numviewports = bpy.props.IntProperty(default=1)

class BLiveDebug(bpy.types.PropertyGroup):
    """Blive Send OSC Debug Messages
    """
    message = bpy.props.StringProperty(default="")

def register():
    print("settings.props.register")
    bpy.utils.register_class(BLiveSettings)
    bpy.utils.register_class(BLiveDebug)

    bpy.types.WindowManager.blive_settings = bpy.props.PointerProperty(type=BLiveSettings)
    bpy.types.WindowManager.blive_debug = bpy.props.PointerProperty(type=BLiveDebug)

    #   initial settings
    #   game engine and GLSL mode
    # throws error in 2.66: AttributeError: '_RestrictContext' object has no attribute 'scene'
    #bpy.context.scene.render.engine = 'BLENDER_GAME'
    #bpy.context.scene.game_settings.material_mode = 'GLSL'

def unregister():
    print("settings.props.unregister")
    bpy.utils.unregister_class(BLiveDebug)
    bpy.utils.unregister_class(BLiveSettings)
