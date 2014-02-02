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

# TODO:
#   *move port in to init script of the logic
#   *move server scripts from logic into scene.pre_draw

import sys
import getopt
import bge
from gameengine import libloserver
from gameengine import logic
from gameengine import render
from gameengine import scene
from gameengine import objects
from gameengine import cameras
from gameengine import lights
from gameengine import meshes
from gameengine import media


def register(port):
    '''registers and starts a osc server inside bge
    '''
    if hasattr(sys, "argv"):
        try:
            index = sys.argv.index('-')
            # check for Blive opts (all args after empty '-')
            if len(sys.argv) > index:
                args = sys.argv[index+1:]
                optlist, args = getopt.getopt(args, 'p:', ['port='])
                for o, a in optlist:
                    if o in ("-p", "--port"):
                        port = int(a)

        except getopt.GetoptError as err:
            print("Error in setting Port parameter, using "%port)

    if not hasattr(bge.logic, "server"):
        bge.logic.server = libloserver.LibloServer(port)
        print("SERVER: ", bge.logic.server.url)

    logic.register()
    render.register()
    scene.register()
    objects.register()
    cameras.register()
    lights.register()
    meshes.register()
    media.register()

    # register server callbacks as last,
    # otherwise the fallback callback will catch all requests
    bge.logic.server.register()
