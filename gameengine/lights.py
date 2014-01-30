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
from gameengine.error import *

class LightRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        if args[0] in sc.lights:
            return (sc.lights[args[0]], attr)
        else:
            raise BLiveError(BLENDDATA_OUTOF_SYNC)


    @classmethod
    def _parse_instance(cls, args):
        return args[:1]

    @classmethod
    def _parse_data(cls, args):
        return args[1:]

def register():
    try:
        bge.logic.server.add_method("/bge/scene/lights/type", "s", LightRequestHandler.reply_int)

        bge.logic.server.add_method("/bge/scene/lights/layer", "si", LightRequestHandler.set_int_value)
        bge.logic.server.add_method("/bge/scene/lights/layer", "s", LightRequestHandler.reply_int)

        bge.logic.server.add_method("/bge/scene/lights/energy", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/energy", "s", LightRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/lights/distance", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/distance", "s", LightRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/lights/color", "sfff", LightRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/bge/scene/lights/color", "s", LightRequestHandler.reply_vec3)

        bge.logic.server.add_method("/bge/scene/lights/lin_attenuation", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/lin_attenuation", "s", LightRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/lights/quad_attenuation", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/quad_attenuation", "s", LightRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/lights/spotsize", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/spotsize", "s", LightRequestHandler.reply_float)

        bge.logic.server.add_method("/bge/scene/lights/spotblend", "sf", LightRequestHandler.set_float_value)
        bge.logic.server.add_method("/bge/scene/lights/spotblend", "s", LightRequestHandler.reply_float)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /bge/scene/lights callbacks - ", err)
