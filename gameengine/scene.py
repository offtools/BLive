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

class SceneRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        return (sc, attr)

    @classmethod
    def _parse_instance(cls, args):
        return None

    @classmethod
    def _parse_data(cls, args):
        if args:
            return args
        else:
            return None

def register():
    try:
        bge.logic.server.add_method("/scene/name", "", SceneRequestHandler.reply_string)
        bge.logic.server.add_method("/scene/objects", "", SceneRequestHandler.reply_names)
        bge.logic.server.add_method("/scene/objectsInactive", "", SceneRequestHandler.reply_names)
        bge.logic.server.add_method("/scene/lights", "", SceneRequestHandler.reply_names)
        bge.logic.server.add_method("/scene/cameras", "", SceneRequestHandler.reply_names)
        bge.logic.server.add_method("/scene/active_camera", "", SceneRequestHandler.reply_string)

        bge.logic.server.add_method("/scene/suspended", "", SceneRequestHandler.reply_bool)
        bge.logic.server.add_method("/scene/activity_culling", "", SceneRequestHandler.reply_bool)

        bge.logic.server.add_method("/scene/activity_culling_radius", "", SceneRequestHandler.reply_float)
        bge.logic.server.add_method("/scene/activity_culling_radius", "f", SceneRequestHandler.set_float_value)

        bge.logic.server.add_method("/scene/dbvt_culling", "", SceneRequestHandler.reply_bool)

        bge.logic.server.add_method("/scene/pre_draw", "", SceneRequestHandler.reply_names)
        bge.logic.server.add_method("/scene/post_draw", "", SceneRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/gravity", "", SceneRequestHandler.reply_vec3)
        bge.logic.server.add_method("/scene/gravity", "fff", SceneRequestHandler.set_vec3_value)

        bge.logic.server.add_method("/scene/addObject", "ss", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/addObject", "ssi", SceneRequestHandler.call_method)

        bge.logic.server.add_method("/scene/end", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/restart", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/replace", "s", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/suspend", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/resume", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/scene/drawObstacleSimulation", "", SceneRequestHandler.call_method)

    except AttributeError:
        print("SERVER: could not register /scene callbacks, no server object")
