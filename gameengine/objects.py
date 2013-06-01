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

class GameObjectRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        if args[0] in sc.objects:
            return (sc.objects[args[0]], attr)
        elif args[0] in sc.objectsInactive:
            return (sc.objectsInactive[args[0]], attr)
        else:
            raise ValueError

    @classmethod
    def _parse_instance(cls, args):
        return args[:1]

    @classmethod
    def _parse_data(cls, args):
        return args[1:]

    # custom handlers
    @classmethod
    def call_alignAxisToVect(cls, path, args, types, source, user_data):
        args = [args[0], (args[1],args[2],args[3]), args[4], args[5]]
        cls._method(path, args, types, source, user_data)

    @classmethod
    def call_getAxisVect(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        cls.call_method_reply_vec3(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfffx_reply_none(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfffx_reply_vec3(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method_reply_vec3(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sffffff_reply_none(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3]), (args[4],args[5],args[6])]
        cls.call_method(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ssx_reply_none(cls, path, args, types, source, user_data):
        nargs = [ args[0], bge.logic.getCurrentScene().objects[args[1]] ]
        for i in args[2:]:
            nargs.append(i)
        cls.call_method(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ssx_reply_f(cls, path, args, types, source, user_data):
        nargs = [ args[0], bge.logic.getCurrentScene().objects[args[1]] ]
        for i in args[2:]:
            nargs.append(i)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfffx_reply_f(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ssx_reply_vec3(cls, path, args, types, source, user_data):
        nargs = [ args[0], bge.logic.getCurrentScene().objects[args[1]] ]
        for i in args[2:]:
            nargs.append(i)
        cls.call_method_reply_vec3(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ssx_reply_string(cls, path, args, types, source, user_data):
        nargs = [ args[0], bge.logic.getCurrentScene().objects[args[1]] ]
        for i in args[2:]:
            nargs.append(i)
        cls.call_method_reply_string(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfffx_reply_string(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method_reply_string(path, nargs, types, source, user_data)

def register():
    try:
        bge.logic.server.add_method("/scene/objects/name", "s", GameObjectRequestHandler.reply_string)

        bge.logic.server.add_method("/scene/objects/mass", "sf", GameObjectRequestHandler.set_float_value)
        bge.logic.server.add_method("/scene/objects/mass", "s", GameObjectRequestHandler.reply_float)

        bge.logic.server.add_method("/scene/objects/linVelocityMin", "sf", GameObjectRequestHandler.set_float_value)
        bge.logic.server.add_method("/scene/objects/linVelocityMin", "s", GameObjectRequestHandler.reply_float)

        bge.logic.server.add_method("/scene/objects/linVelocityMax", "sf", GameObjectRequestHandler.set_float_value)
        bge.logic.server.add_method("/scene/objects/linVelocityMax", "s", GameObjectRequestHandler.reply_float)

        bge.logic.server.add_method("/scene/objects/localInertia", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/parent", "s", GameObjectRequestHandler.reply_string)

        bge.logic.server.add_method("/scene/objects/groupMembers", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/groupObject", "s", GameObjectRequestHandler.reply_string)

        bge.logic.server.add_method("/scene/objects/scene", "s", GameObjectRequestHandler.reply_string)

        bge.logic.server.add_method("/scene/objects/visible", "si", GameObjectRequestHandler.set_bool_value)
        bge.logic.server.add_method("/scene/objects/visible", "s", GameObjectRequestHandler.reply_bool)

        bge.logic.server.add_method("/scene/objects/color", "sffff", GameObjectRequestHandler.set_vec4_value)
        bge.logic.server.add_method("/scene/objects/color", "s", GameObjectRequestHandler.reply_vec4)

        bge.logic.server.add_method("/scene/objects/occlusion", "si", GameObjectRequestHandler.set_bool_value)
        bge.logic.server.add_method("/scene/objects/occlusion", "s", GameObjectRequestHandler.reply_bool)

        bge.logic.server.add_method("/scene/objects/position", "s", GameObjectRequestHandler.reply_vec3)
        bge.logic.server.add_method("/scene/objects/position", "sfff", GameObjectRequestHandler.set_vec3_value)

        bge.logic.server.add_method("/scene/objects/orientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/orientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        bge.logic.server.add_method("/scene/objects/scaling", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/scaling", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/localOrientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/localOrientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        bge.logic.server.add_method("/scene/objects/worldOrientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/worldOrientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        bge.logic.server.add_method("/scene/objects/localScale", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/localScale", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/worldScale", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/worldScale", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/localPosition", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/localPosition", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/worldPosition", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/worldPosition", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/localTransform", "sfff", GameObjectRequestHandler.set_matrix4x4_value)
        bge.logic.server.add_method("/scene/objects/localTransform", "s", GameObjectRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/scene/objects/worldTransform", "sfff", GameObjectRequestHandler.set_matrix4x4_value)
        bge.logic.server.add_method("/scene/objects/worldTransform", "s", GameObjectRequestHandler.reply_matrix4x4)

        bge.logic.server.add_method("/scene/objects/localLinearVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/localLinearVelocity", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/worldLinearVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/worldLinearVelocity", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/localAngularVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/localAngularVelocity", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/worldAngularVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        bge.logic.server.add_method("/scene/objects/worldAngularVelocity", "s", GameObjectRequestHandler.reply_vec3)

        bge.logic.server.add_method("/scene/objects/timeOffset", "sf", GameObjectRequestHandler.set_float_value)
        bge.logic.server.add_method("/scene/objects/timeOffset", "s", GameObjectRequestHandler.reply_float)

        bge.logic.server.add_method("/scene/objects/state", "si", GameObjectRequestHandler.set_int_value)
        bge.logic.server.add_method("/scene/objects/state", "s", GameObjectRequestHandler.reply_int)

        bge.logic.server.add_method("/scene/objects/meshes", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/sensors", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/controllers", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/actuators", "s", GameObjectRequestHandler.reply_names)

        #TODO
        #bge.logic.server.add_method("/scene/objects/attrDict", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/children", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/childrenRecursive", "s", GameObjectRequestHandler.reply_names)

        bge.logic.server.add_method("/scene/objects/life", "sf", GameObjectRequestHandler.set_float_value)
        bge.logic.server.add_method("/scene/objects/life", "s", GameObjectRequestHandler.reply_float)

        bge.logic.server.add_method("/scene/objects/endObject", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/replaceMesh", "ssii", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/setOcclusion", "sii", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/alignAxisToVect", "sfffif", GameObjectRequestHandler.call_alignAxisToVect)

        bge.logic.server.add_method("/scene/objects/getAxisVect", "sfff", GameObjectRequestHandler.call_getAxisVect)

        bge.logic.server.add_method("/scene/objects/applyMovement", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/applyMovement", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/applyRotation", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/applyRotation", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/applyForce", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/applyForce", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/applyTorque", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/applyTorque", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/getLinearVelocity", "si", GameObjectRequestHandler.call_method_reply_vec3)
        bge.logic.server.add_method("/scene/objects/getLinearVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        bge.logic.server.add_method("/scene/objects/setLinearVelocity", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/setLinearVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/getAngularVelocity", "si", GameObjectRequestHandler.call_method_reply_vec3)
        bge.logic.server.add_method("/scene/objects/getAngularVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        bge.logic.server.add_method("/scene/objects/setAngularVelocity", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        bge.logic.server.add_method("/scene/objects/setAngularVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        bge.logic.server.add_method("/scene/objects/getVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_vec3)
        bge.logic.server.add_method("/scene/objects/getVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        bge.logic.server.add_method("/scene/objects/getReactionForce", "s", GameObjectRequestHandler.call_method_reply_vec3)

        bge.logic.server.add_method("/scene/objects/applyImpulse", "sffffff", GameObjectRequestHandler.call_method_sffffff_reply_none)

        bge.logic.server.add_method("/scene/objects/suspendDynamics", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/restoreDynamics", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/enableRigidBody", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/disableRigidBody", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/setParent", "ssii", GameObjectRequestHandler.call_method_ssx_reply_none)
        bge.logic.server.add_method("/scene/objects/setParent", "ssi", GameObjectRequestHandler.call_method_ssx_reply_none)
        bge.logic.server.add_method("/scene/objects/setParent", "ss", GameObjectRequestHandler.call_method_ssx_reply_none)

        bge.logic.server.add_method("/scene/objects/removeParent", "s", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/getPhysicsId", "s", GameObjectRequestHandler.call_method_reply)

        bge.logic.server.add_method("/scene/objects/getPropertyNames", "s", GameObjectRequestHandler.call_method_reply_names)

        bge.logic.server.add_method("/scene/objects/getDistanceTo", "ss", GameObjectRequestHandler.call_method_ssx_reply_f)
        bge.logic.server.add_method("/scene/objects/getDistanceTo", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_f)

        bge.logic.server.add_method("/scene/objects/getVectTo", "ss", GameObjectRequestHandler.call_method_ssx_reply_vec3)
        bge.logic.server.add_method("/scene/objects/getVectTo", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_vec3)

        bge.logic.server.add_method("/scene/objects/rayCastTo", "ssfs", GameObjectRequestHandler.call_method_ssx_reply_string)
        bge.logic.server.add_method("/scene/objects/rayCastTo", "sffffs", GameObjectRequestHandler.call_method_sfffx_reply_string)

# TODO: /scene/objects/rayCast
#       bge.logic.server.add_method("/scene/objects/rayCast", "ssffffsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)
#       bge.logic.server.add_method("/scene/objects/rayCast", "sfffsfsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)
#       bge.logic.server.add_method("/scene/objects/rayCast", "sfffffffsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)

        bge.logic.server.add_method("/scene/objects/setCollisionMargin", "sf", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/sendMessage", "ssss", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/reinstancePhysicsMesh", "sss", GameObjectRequestHandler.call_method_reply_bool)

        bge.logic.server.add_method("/scene/objects/playAction", "sff", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffi", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffii", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffiif", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffiifi", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffiifif", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "sffiififi", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/playAction", "s", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/playAction", "si", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/getActionFrame", "si", GameObjectRequestHandler.call_method_reply)
        bge.logic.server.add_method("/scene/objects/getActionFrame", "s", GameObjectRequestHandler.call_method_reply)

        bge.logic.server.add_method("/scene/objects/setActionFrame", "sif", GameObjectRequestHandler.call_method)
        bge.logic.server.add_method("/scene/objects/setActionFrame", "si", GameObjectRequestHandler.call_method)

        bge.logic.server.add_method("/scene/objects/isPlayingAction", "si", GameObjectRequestHandler.call_method_reply_bool)
        bge.logic.server.add_method("/scene/objects/isPlayingAction", "s", GameObjectRequestHandler.call_method_reply_bool)

    except AttributeError:
        print("SERVER: could not register /scene/objects callbacks, no server object")
