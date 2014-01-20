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


#
#   Blender OSC-BGE addon, this addon allows to send changes from blender
#   to a running gameengine instance
#

bl_info = {
    "name": "BLive",
    "author": "offtools",
    "version": (0, 0, 1),
    "blender": (2, 6, 4),
    "location": "various Panels with prefix BLive",
    "description": "blender to bge osc network addon",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine"}

# import modules
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(viewport)
    #imp.reload(client)
    #imp.reload(texture)
    imp.reload(marker)
    imp.reload(object)
    #imp.reload(material)
else:
    from . import common
    from . import viewport
    #from . import client
    #from . import texture
    from . import marker
    from . import object
    #from . import material

import bpy

def register():
    print("__init__.register")
    common.register()
    viewport.register()
    #client.register()
    #texture.register()
    marker.register()
    object.register()
    #material.register()

def unregister():
    print("__init__.unregister")
    #material.unregister()
    object.unregister()
    marker.unregister()
    #texture.unregister()
    #client.unregister()
    viewport.unregister()
    common.unregister()

if __name__ == "__main__":
    pass
