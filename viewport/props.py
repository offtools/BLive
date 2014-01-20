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

# TODO: user operators instead calling BLiveClient

import bpy

class BLiveViewport(bpy.types.PropertyGroup):
    m_active = bpy.props.BoolProperty(default=False)
    m_left = bpy.props.IntProperty(default=0)
    m_right = bpy.props.IntProperty(default=0)
    m_top = bpy.props.IntProperty(default=0)
    m_bottom = bpy.props.IntProperty(default=0)

def register():
    print("viewport.props.register")

    #bpy.types.Camera.viewport = bpy.props.PointerProperty(type=BLiveViewport, options={"HIDDEN"})

def unregister():
    print("viewport.props.unregister")

    del bpy.types.Camera.viewport
    #bpy.utils.unregister_class(BLiveViewport)
