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

#TODO:
#gameobject - attrDict, properties, rayCast
#use only one method_reply
#
#errors: use only BLiveError

# TODO: projection matrix stored in blendfile is not used on startup
#       it needs to be set after connecting with first client (send / recieve init data)

#OSC Paths:
#path('/bge/scene/attr', [args, ...])
#scene: obj=None
#path('/bge/scene/objects/attr', 'Object', [args, ...])
#object: obj=bge.logic.getCurrentScene().objects[args[0]]
#path('/bge/scene/objects/meshes/attr', 'Object', 0, [args, ...])
#mesh: obj=bge.logic.getCurrentScene().objects[args[0]].meshes[args[1]]
#path('/bge/scene/objects/meshes/material/attr', 'Object', 0, 0, [args, ...])
#material: obj=bge.logic.getCurrentScene().objects[args[0]].meshes[args[1]].materials[args[2]]


import bge
from liblo import Server, UDP
from gameengine.requesthandler import *

class LibloServer(Server):
    def __init__(self, port, proto=UDP):
        super().__init__(port, proto)
        self.clients = set()

    def register(self):
        self.add_method("/bge/connect", '', self.cb_connect)
        self.add_method("/bge/shutdown", '', self.cb_shutdown)
        self.add_method(None, None, self.cb_fallback)

    def cb_connect(self, path, args, types, source, user_data):
        print("SERVER: received client connect: ", source.url)
        self.clients.add(source.url)
        self.send(source.url, "/bge/srvinfo", self.url, bge.render.getWindowWidth(), bge.render.getWindowHeight())

    def cb_fallback(self, path, args, types, source, user_data):
        print ("SERVER_ received message: ", path, args, types, source.url, user_data)
        self.send(source.url, "/bge/error", "unknown message")

    def cb_shutdown(self, path, args, types, source, user_data):
        print("SERVER: Shutting down")
        for i in self.clients:
            self.send(i, "/bge/shutdown", source.url)
        bge.logic.endGame()
