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
from ..client import BLiveClient

# TODO: poll method
class BLive_OT_osc_object_diffuse_color(bpy.types.Operator):
    """
        Operator - send object diffuse color
    """
    bl_idname = "blive.osc_object_diffuse_color"
    bl_label = "BLive - send diffuse color and transparency"
    obname = bpy.props.StringProperty()

    def execute(self, context):
        ob = context.scene.objects[self.obname]
        mat = ob.active_material
        ob.color[0] = mat.diffuse_color[0]
        ob.color[1] = mat.diffuse_color[1]
        ob.color[2] = mat.diffuse_color[2]
        ob.color[3] = mat.alpha
        BLiveClient().send("/data/object/color", [self.obname, mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2], mat.alpha])
        return{'FINISHED'}

# TODO: poll method, move to object
class BLive_OT_osc_object_obcolor(bpy.types.Operator):
    """
        Operator - send obcolor
    """
    bl_idname = "blive.osc_object_obcolor"
    bl_label = "BLive - send object color"
    obname = bpy.props.StringProperty()

    def execute(self, context):
        ob = context.scene.objects[self.obname]
        BLiveClient().send("/data/object/color", [self.obname, ob.color[0], ob.color[1], ob.color[2], ob.color[3]])
        return{'FINISHED'}

def register():
    print("material.ops.register")
    bpy.utils.register_class(BLive_OT_osc_object_diffuse_color)
    bpy.utils.register_class(BLive_OT_osc_object_obcolor)

def unregister():
    print("material.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_osc_object_diffuse_color)
    bpy.utils.unregister_class(BLive_OT_osc_object_obcolor)
