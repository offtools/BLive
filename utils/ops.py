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
import sys
import imp

class BLive_OT_reimport_script(bpy.types.Operator):
    '''reimport script'''

    bl_idname = "blive.reimport_script"
    bl_label = "BLive reimport script"
    bl_options = {'REGISTER', 'UNDO'}

    module = bpy.props.StringProperty()

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        if self.module in context.blend_data.texts and self.module[:-3] in sys.modules:
            imp.reload(sys.modules[self.module[:-3]])
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

def register():
    print("utils.ops.register")
    bpy.utils.register_class(BLive_OT_reimport_script)

def unregister():
    print("utils.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_reimport_script)
