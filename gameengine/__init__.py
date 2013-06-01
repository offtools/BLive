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

import sys
import getopt
import bge
from gameengine import libloserver
from gameengine import scene
from gameengine import objects
from gameengine import camera


_PORT = 9901

def register():
    '''registers and starts a osc server inside bge
    '''

    try:
        index = sys.argv.index('-')

        # check for Blive opts (all args after empty '-')
        if len(sys.argv) > index:
            args = sys.argv[index+1:]
            optlist, args = getopt.getopt(args, 'p:', ['port='])
            for o, a in optlist:
                if o in ("-p", "--port"):
                    _PORT = int(a)

    except getopt.GetoptError as err:
        print("Error in setting Port using"%_PORT)

    if not hasattr(bge.logic, "server"):
        bge.logic.server = libloserver.LibloServer(_PORT)
        print(bge.logic.server.url)

        scene.register()
        objects.register()
        camera.register()

        bge.logic.server.register()
