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
import math
import bmesh
from liblo import Bundle, Message
from bpy.app.handlers import persistent
from ..common.libloclient import Client
from . import ops

@persistent
def object_update_handler(scene):
    if scene.is_updated:
        print("Scene updated")

    # check objects updates
    for ob in scene.objects:
        if ob.is_updated:
            bundle = Bundle()
            bundle.add(Message("/scene/objects/position", ob.name, ob.location[0], ob.location[1], ob.location[2]))
            bundle.add(Message("/scene/objects/orientation", ob.name, ob.rotation_euler[0], ob.rotation_euler[1], ob.rotation_euler[2]))

            if ob.type == 'MESH':
                bundle.add(Message("/scene/objects/scaling", ob.name, ob.scale[0], ob.scale[1], ob.scale[2]))

            Client().send(bundle)

        if ob.is_updated_data:
            if ob.type == 'CAMERA':
                camera = ob.data
                bundle = Bundle()

                e = 1.0/math.tan(camera.angle/2.0)
                a = bpy.context.scene.game_settings.resolution_y/bpy.context.scene.game_settings.resolution_x
                n = camera.clip_start
                f = camera.clip_end

                msg_matrix = Message('/scene/cameras/projection_matrix')

                msg_matrix.add(camera.name,
                               e, 0.0, 2.0*camera.shift_x, 0.0,
                               0.0, e/a, 2.0*camera.shift_y/a, 0.0,
                               0.0, 0.0, (f+n)/(n-f), (2*f*n)/(n-f),
                               0.0, 0.0, -1.0, 0.0
                               )


                perspective = 1
                if camera.type == 'ORTHO':
                    perspective = 0
                msg_persp = Message('/scene/cameras/perspective')
                msg_persp.add(camera.name, perspective)

                bundle.add(msg_persp)
                bundle.add(msg_matrix)
                Client().send(bundle)

            elif ob.type == 'LAMP':
                lamp = ob.data
                #ops.osc_object_lamp(lamp)

            elif ob.type == 'MESH' and ob.mode == 'EDIT':
                #operators seems much slower, we call classmedthod of Op directly
                ops.BLive_OT_osc_object_meshdata.update_mesh(ob)

def register():
    print("object.handler.register")
    Client().add_apphandler('scene_update_post', object_update_handler)

def unregister():
    print("object.handler.unregister")
