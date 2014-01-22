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

from gameengine.requesthandler import *

class CameraRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        if args[0] in sc.cameras:
            return (sc.cameras[args[0]], attr)
        else:
            raise ValueError

    @classmethod
    def _parse_instance(cls, args):
        return args[:1]

    @classmethod
    def _parse_data(cls, args):
        return args[1:]

    @classmethod
    def call_method_sfffx_reply(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_s24f_reply(cls, path, args, types, source, user_data):
        nargs = [args[0]]
        box = [[nargs[i*3+1], nargs[i*3+2], nargs[i*3+3]] for i in range(8)]
        nargs.append(box)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_siiii_reply_none(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ss_reply_vec2(cls, path, args, types, source, user_data):
        nargs = [args[0], bge.logic.getCurrentScene().objects[args[1]]]
        cls.call_method_reply_vec2(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfff_reply_vec2(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method_reply_vec2(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sff_reply_vec3(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method_reply_vec3(path, nargs, types, source, user_data)

def register():
    try:
        bge.logic.server.add_method("/bge/scene/cameras/lens", "sf", CameraRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/cameras/lens", "s", CameraRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/cameras/ortho_scale", "sf", CameraRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/cameras/ortho_scale", "s", CameraRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/cameras/near", "sf", CameraRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/cameras/near", "s", CameraRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/cameras/far", "sf", CameraRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/cameras/far", "s", CameraRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/cameras/perspective", "si", CameraRequestHandler.set_bool_value)
        bge.logic.server.add_method("/bge/scene/cameras/perspective", "s", CameraRequestHandler.reply_bool)

        bge.logic.server.add_method("/bge/scene/cameras/frustum_culling", "si", CameraRequestHandler.set_bool_value)
        bge.logic.server.add_method("/bge/scene/cameras/frustum_culling", "s", CameraRequestHandler.reply_bool)

        bge.logic.server.add_method("/bge/scene/cameras/projection_matrix", "sffffffffffffffff", CameraRequestHandler.set_matrix4x4_value)
        bge.logic.server.add_method("/bge/scene/cameras/projection_matrix", "s", CameraRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/model_matrix", "s", CameraRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/camera_to_world", "s", CameraRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/world_to_camera", "s", CameraRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/useViewport", "si", CameraRequestHandler.set_bool_value)

        bge.logic.server.add_method("/bge/scene/cameras/sphereInsideFrustum", "sffff", CameraRequestHandler.call_method_sfffx_reply)

        bge.logic.server.add_method("/bge/scene/cameras/boxInsideFrustum", "sffffffffffffffffffffffff", CameraRequestHandler.call_method_s24f_reply)

        bge.logic.server.add_method("/bge/scene/cameras/pointInsideFrustum", "sfff", CameraRequestHandler.call_method_sfffx_reply)

        bge.logic.server.add_method("/bge/scene/cameras/getCameraToWorld", "s", CameraRequestHandler.call_method_reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/getWorldToCamera", "s", CameraRequestHandler.call_method_reply_matrix4x4)

        bge.logic.server.add_method("/bge/scene/cameras/setOnTop", "s", CameraRequestHandler.call_method)

        bge.logic.server.add_method("/bge/scene/cameras/setViewport", "siiii", CameraRequestHandler.call_method_reply)

        bge.logic.server.add_method("/bge/scene/cameras/getScreenPosition", "ss", CameraRequestHandler.call_method_ss_reply_vec2)
        bge.logic.server.add_method("/bge/scene/cameras/getScreenPosition", "sfff", CameraRequestHandler.call_method_sfff_reply_vec2)

        bge.logic.server.add_method("/bge/scene/cameras/getScreenVect", "sff", CameraRequestHandler.call_method_sff_reply_vec3)

        bge.logic.server.add_method("/bge/scene/cameras/getScreenRay", "sfffs", CameraRequestHandler.call_method_reply_name)
        bge.logic.server.add_method("/bge/scene/cameras/getScreenRay", "sfff", CameraRequestHandler.call_method_reply_name)


    except AttributeError as err:
        print("SERVER: could not register /bge/scene/cameras reason: ", err)
