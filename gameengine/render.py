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
        attr = path.split('/')[-1:][0]
        return (bge.render, attr)

    @classmethod
    def _parse_instance(cls, args):
        return None

    @classmethod
    def _parse_data(cls, args):
        if args:
            return args
        else:
            return None

    @classmethod
    def call_method_vec(cls, path, args, types, source, user_data):
        cls.call_method(path, [args], types, source, user_data)

    @classmethod
    def call_method_3vec3(cls, path, args, types, source, user_data):
        cls.call_method(path, [args[0:3],args[3:6], args[6:9]], types, source, user_data)

def register():
    try:
        bge.logic.server.add_method("/bge/render/getWindowWidth", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/getWindowHeight", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setWindowSize", "ii", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setFullScreen", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getFullScreen", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/makeScreenshot", "s", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/enableVisibility", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/showMouse", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setMousePosition", "ii", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setBackgroundColor", "ffff", SceneRequestHandler.call_method_vec)
        bge.logic.server.add_method("/bge/render/setMistColor", "fff", SceneRequestHandler.call_method_vec)
        bge.logic.server.add_method("/bge/render/setAmbientColor", "fff", SceneRequestHandler.call_method_vec)
        bge.logic.server.add_method("/bge/render/setMistStart", "f", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setMistEnd", "f", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/disableMist", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setEyeSeparation", "f", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getEyeSeparation", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setFocalLength", "f", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/bge.render.getFocalLength", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setMaterialMode", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getMaterialMode", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setGLSLMaterialSetting", "si", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getGLSLMaterialSetting", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setAnisotropicFiltering", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getAnisotropicFiltering", "", SceneRequestHandler.call_method_reply)
        bge.logic.server.add_method("/bge/render/setMipmapping", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getMipmapping", "", SceneRequestHandler.call_method_reply)
        # drawLine needs to be called every frame (KXScene.postdraw)
        #bge.logic.server.add_method("/bge/render/drawLine", "fffffffff", SceneRequestHandler.call_method_3vec3)
        bge.logic.server.add_method("/bge/render/enableMotionBlur", "f", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/disableMotionBlur", "", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/setVsync", "i", SceneRequestHandler.call_method)
        bge.logic.server.add_method("/bge/render/getVsync", "", SceneRequestHandler.call_method_reply)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /bge/render callbacks - ", err)
