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

#TODO: Add camera property to projection matrix operator

import bpy
import math
import bmesh
from liblo import Bundle, Message
from ..common.libloclient import Client

class BLive_OT_osc_camera_projectionmatrix(bpy.types.Operator):
    """
        Operator - send camera data, projection matrix
    """
    bl_idname = "blive.osc_camera_projectionmatrix"
    bl_label = "BLive - send camera projectionmatrix"
    camera = bpy.props.StringProperty(default='')

    @classmethod
    def poll(self, context):
        return bool(context.scene.camera)

    @classmethod
    def update_projectionmatrix(self, camera):
        data = camera.data
        # operators seems much slower, we add a classmedthod to call the code directly for internal use (see handler.py)
        bundle = Bundle()

        e = 1.0/math.tan(data.angle/2.0)
        a = bpy.context.scene.game_settings.resolution_y/bpy.context.scene.game_settings.resolution_x
        n = data.clip_start
        f = data.clip_end

        msg_matrix = Message('/bge/scene/cameras/projection_matrix')

        msg_matrix.add(camera.name,
                       e, 0.0, 2.0*data.shift_x, 0.0,
                       0.0, e/a, 2.0*data.shift_y/a, 0.0,
                       0.0, 0.0, (f+n)/(n-f), (2*f*n)/(n-f),
                       0.0, 0.0, -1.0, 0.0
                       )

        perspective = 1
        if data.type == 'ORTHO':
            perspective = 0
        msg_persp = Message('/bge/scene/cameras/perspective')
        msg_persp.add(camera.name, perspective)

        bundle.add(msg_persp)
        bundle.add(msg_matrix)
        Client().send(bundle)

    def execute(self, context):
        try:
            if self.camera:
                self.update_projectionmatrix(context.scene.objects[self.camera])
            else:
                self.update_projectionmatrix(context.scene.camera)
            return{'FINISHED'}
        except KeyError:
            print("ERROR: Camera: %s not found"%self.camera)
            return{'CANCELED'}

class BLive_OT_osc_object_lamp(bpy.types.Operator):
    """
        Operator - send lamp data
    """
    bl_idname = "blive.osc_object_lamp"
    bl_label = "BLive - send lamp data"

    @classmethod
    def poll(self, context):
        return context.active_object and context.active_object.type == 'LAMP'

    @classmethod
    def update_lamp(self, lamp):
        data = lamp.data
        bundle = Bundle()
        bundle.add(Message("/bge/scene/lights/energy", lamp.name, data.energy))
        bundle.add(Message("/bge/scene/lights/color", lamp.name, data.color[0], data.color[1], data.color[2]))
        if data.type == 'POINT':
            bundle.add(Message("/bge/scene/lights/distance", lamp.name, data.distance))
            bundle.add(Message("/bge/scene/lights/lin_attenuation", lamp.name, data.linear_attenuation))
            bundle.add(Message("/bge/scene/lights/quad_attenuation", lamp.name, data.quadratic_attenuation))
        elif data.type == 'SPOT':
            bundle.add(Message("/bge/scene/lights/distance", lamp.name, data.distance))
            bundle.add(Message("/bge/scene/lights/lin_attenuation", lamp.name, data.linear_attenuation))
            bundle.add(Message("/bge/scene/lights/quad_attenuation", lamp.name, data.quadratic_attenuation))
            bundle.add(Message("/bge/scene/lights/spotsize", lamp.name, math.degrees(data.spot_size)))
            bundle.add(Message("/bge/scene/lights/spotblend", lamp.name, data.spot_blend))
        Client().send(bundle)

    def execute(self, context):
        print("UPDATE LAMP, ", context.active_object)
        self.update_lamp(context.active_object)
        return{'FINISHED'}

class BLive_OT_osc_object_meshdata(bpy.types.Operator):
    """
        Operator - send mesh data
    """
    bl_idname = "blive.osc_object_meshdata"
    bl_label = "BLive - send meshdata"

    @classmethod
    def poll(self, context):
        return context.active_object and context.active_object.type == 'MESH' and C.active_object.mode == 'EDIT'

    @classmethod
    def update_mesh(self, ob):
        data = ob.data
        # operators seems much slower, we add a classmedthod to call the code directly for internal use (see handler.py)
        mesh = bmesh.from_edit_mesh(data)
        mesh_index = 0
        bundle = Bundle()
        for face in mesh.faces:
            for vindex, vertex in enumerate(face.verts):
                bundle.add(Message("/bge/scene/objects/meshes/update", ob.name, mesh_index, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2]))
        Client().send(bundle)

    def execute(self, context):
        self.update_mesh(context.active_object)
        return{'FINISHED'}

def register():
    print("object.ops.register")
    bpy.utils.register_class(BLive_OT_osc_camera_projectionmatrix)
    bpy.utils.register_class(BLive_OT_osc_object_lamp)
    bpy.utils.register_class(BLive_OT_osc_object_meshdata)

def unregister():
    print("object.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_osc_camera_projectionmatrix)
    bpy.utils.unregister_class(BLive_OT_osc_object_lamp)
    bpy.utils.unregister_class(BLive_OT_osc_object_meshdata)
