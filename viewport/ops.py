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
from liblo import Bundle, Message
from ..common.libloclient import Client

class BLive_OT_osc_update_viewports(bpy.types.Operator):
    """
        Operator - update bge viewports
    """
    bl_idname = "blive.osc_update_viewports"
    bl_label = "BLive - update Viewports"

    @classmethod
    def poll(self, context):
        return bool(context.scene.camera)

    def execute(self, context):
        settings = context.window_manager.blive_settings
        active_camera = context.scene.camera

        # count Viewports
        n = len([i for i in context.scene.objects if i.type == 'CAMERA' and i.data.viewport.active])
        if n == 0:
            active_camera.data.viewport.active = True
            settings.numviewports = 1
        else:
            settings.numviewports = n

        vpcam = [i for i in context.scene.objects if i.type == 'CAMERA' and i.data.viewport.active]
        bundle = Bundle()
        for cam in vpcam:
            vp = cam.data.viewport
            bundle.add(Message("/bge/scene/cameras/setViewport", cam.name, vp.left, vp.bottom, vp.right, vp.top))
            bundle.add(Message("/bge/scene/cameras/useViewport", cam.name, int(vp.active)))
        Client().send(bundle)

        return{'FINISHED'}

def register():
    print("viewport.ops.register")
    bpy.utils.register_class(BLive_OT_osc_update_viewports)

def unregister():
    print("viewport.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_osc_update_viewports)
