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
from gameengine.error import BLiveError

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
        bge.logic.server.add_method("/bge/scene/name", "", SceneRequestHandler.reply_name)
        bge.logic.server.add_method("/bge/scene/objects", "", SceneRequestHandler.reply_namelist)
        bge.logic.server.add_method("/bge/scene/objectsInactive", "", SceneRequestHandler.reply_namelist)
        bge.logic.server.add_method("/bge/scene/lights", "", SceneRequestHandler.reply_namelist)
        bge.logic.server.add_method("/bge/scene/cameras", "", SceneRequestHandler.reply_namelist)
        bge.logic.server.add_method("/bge/scene/active_camera", "", SceneRequestHandler.reply_string)

        bge.logic.server.add_method("/bge/scene/suspended", "", SceneRequestHandler.reply_bool)
        bge.logic.server.add_method("/bge/scene/activity_culling", "", SceneRequestHandler.reply_bool)

        bge.logic.server.add_method("/bge/scene/activity_culling_radius", "", SceneRequestHandler.reply_float)
        bge.logic.server.add_method("/bge/scene/activity_culling_radius", "f", SceneRequestHandler.set_float_value)

        bge.logic.server.add_method("/bge/scene/dbvt_culling", "", SceneRequestHandler.reply_bool)

        bge.logic.server.add_method("/bge/scene/pre_draw", "", SceneRequestHandler.reply_namelist)
        bge.logic.server.add_method("/bge/scene/post_draw", "", SceneRequestHandler.reply_namelist)

        bge.logic.server.add_method("/bge/scene/gravity", "", SceneRequestHandler.reply_vec3)
        bge.logic.server.add_method("/bge/scene/gravity", "fff", SceneRequestHandler.set_vec3_value)

        bge.logic.server.add_method("/bge/scene/addObject", "ss", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/addObject", "ssi", SceneRequestHandler.call_method)

        bge.logic.server.add_method("/bge/scene/end", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/restart", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/replace", "s", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/suspend", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/resume", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/scene/drawObstacleSimulation", "", SceneRequestHandler.call_method)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /scene callbacks - ", err)
