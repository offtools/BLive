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

import bge
from gameengine.requesthandler import *

class SceneRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        attr = path.split('/')[-1:][0]
        return (bge.logic, attr)

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
    def call_startGame(cls, path, args, types, source, user_data):
        bge.logic.server.free()
        del bge.logic.server
        cls.call_method(path, args, types, source, user_data)

    @classmethod
    def call_endGame(cls, path, args, types, source, user_data):
        bge.logic.server.shutdown(source)
        cls.call_method(path, args, types, source, user_data)

    @classmethod
    def call_restartGame(cls, path, args, types, source, user_data):
        bge.logic.server.free()
        del bge.logic.server
        cls.call_method(path, args, types, source, user_data)

    @classmethod
    def call_LibLoad(cls, path, args, types, source, user_data):
        cls.call_method(path, [args[0], args[1], None, args[2], args[3], args[4], args[5]], types, source, user_data)

def register():
    try:
        bge.logic.server.add_method("/bge/logic/startGame", "s", SceneRequestHandler.call_startGame)
        bge.logic.server.add_method("/bge/logic/endGame", "", SceneRequestHandler.call_endGame)
        bge.logic.server.add_method("/bge/logic/restartGame", "", SceneRequestHandler.call_restartGame)
        #bge.logic.server.add_method("/bge/logic/LibLoad", "sssiii", SceneRequestHandler.call_LibLoad)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /bge/logic callbacks - ", err)
