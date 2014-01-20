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

class MeshRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        if args[0] in sc.objects:
            ob = sc.objects[args[0]]
            if  args[1] >= 0 and args[1] < len(ob.meshes):
                return (ob.meshes[args[1]], attr)
            else:
                raise ValueError
        else:
            raise ValueError

    @classmethod
    def _parse_instance(cls, args):
        return args[:1]

    @classmethod
    def _parse_data(cls, args):
        return args[1:]

    @classmethod
    def call_method_update(cls, path, args, types, source, user_data):
        scene = bge.logic.getCurrentScene()
        ob = scene.objects[args[0]]
        mesh_index = args[1]
        polygon_index = args[2]
        vertex_index = args[3]
        x = args[4]
        y = args[5]
        z = args[6]

        #   retrieve polygon
        polygon = ob.meshes[0].getPolygon(polygon_index)

        #   get verts from polygon
        verts = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
        if verts[3] == 0: verts.pop()

        #   get material index (workaround for matid bug, matid is not an attr of KX_PolyProxy)
        mat_index = ob.meshes[0].materials.index(polygon.material)
        mesh = ob.meshes[0]
        try:
            vertex = mesh.getVertex(mat_index, verts[vertex_index])
            vertex.setXYZ([x,y,z])
        except IndexError as err:
            print("%s : mat_idx: %d vert_idx: %d" %(err, mat_index, vertex_index))

def register():
    try:
        #bge.logic.server.add_method("/bge/scene/objects/meshes/materials", "si", MeshRequestHandler.reply_)
        bge.logic.server.add_method("/bge/scene/objects/meshes/numPolygons", "si", MeshRequestHandler.reply_int)
        bge.logic.server.add_method("/bge/scene/objects/meshes/numMaterials", "si", MeshRequestHandler.reply_int)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getNumMaterials", "si", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getMaterialName", "sii", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getTextureName", "sii", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getVertexArrayLength", "sii", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getVertexArrayLength", "sii", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getVertex", "siii", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getNumPolygons", "si", MeshRequestHandler.reply_)
        #bge.logic.server.add_method("/bge/scene/objects/meshes/getPolygon", "sii", MeshRequestHandler.reply_)

        #extra update method (using bmesh in blender)
        bge.logic.server.add_method("/bge/scene/objects/meshes/update", "siiifff", MeshRequestHandler.call_method_update)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /bge/scene/objects/meshes callbacks - ", err)
