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


#OSC Paths:
#path('/scene/attr', [args, ...])
#scene: obj=None
#path('/scene/objects/attr', 'Object', [args, ...])
#object: obj=bge.logic.getCurrentScene().objects[args[0]]
#path('/scene/objects/meshes/attr', 'Object', 0, [args, ...])
#mesh: obj=bge.logic.getCurrentScene().objects[args[0]].meshes[args[1]]
#path('/scene/objects/meshes/material/attr', 'Object', 0, 0, [args, ...])
#material: obj=bge.logic.getCurrentScene().objects[args[0]].meshes[args[1]].materials[args[2]]


import bge
from liblo import Server, Message, UDP
from .error import BLiveError

#
# Default Attribute Handler
#

class AttributeType():
    @classmethod
    def get(cls, obj, attr):
        return [obj.__getattribute__(attr)]

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, args)

class AttributeTypeString(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        val = obj.__getattribute__(attr)
        if val:
            return [str(obj.__getattribute__(attr))]
        else:
            return ['']

class AttributeNames(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        try:
            return [", ".join([i.name for i in obj.__getattribute__(attr)])]
        except TypeError:
            return ['']

class AttributeObject(AttributeType):
    @classmethod
    def set(cls, obj, attr, args):
        pass

class AttributeTypeBool(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return [int(obj.__getattribute__(attr))]

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, bool(args[0]))

class AttributeTypeInt(AttributeType):
    pass

class AttributeTypeFloat(AttributeType):
    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, args[0])

class AttributeTypeVec3(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return [obj.__getattribute__(attr)[0],
                obj.__getattribute__(attr)[1],
                obj.__getattribute__(attr)[2]]

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, (args[0:3]))

class AttributeTypeVec4(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return [obj.__getattribute__(attr)[0],
                obj.__getattribute__(attr)[1],
                obj.__getattribute__(attr)[2],
                obj.__getattribute__(attr)[3]]

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, (args[0:4]))

class AttributeTypeMatrix3x3(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return (obj.__getattribute__(attr)[0][0],
                obj.__getattribute__(attr)[0][1],
                obj.__getattribute__(attr)[0][2],
                obj.__getattribute__(attr)[1][0],
                obj.__getattribute__(attr)[1][1],
                obj.__getattribute__(attr)[1][2],
                obj.__getattribute__(attr)[2][0],
                obj.__getattribute__(attr)[2][1],
                obj.__getattribute__(attr)[2][2])

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, (args[0:3],args[3:6],args[6:9]))

class AttributeTypeMatrix4x4(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return (obj.__getattribute__(attr)[0][0],
                obj.__getattribute__(attr)[0][1],
                obj.__getattribute__(attr)[0][2],
                obj.__getattribute__(attr)[0][3],
                obj.__getattribute__(attr)[1][0],
                obj.__getattribute__(attr)[1][1],
                obj.__getattribute__(attr)[1][2],
                obj.__getattribute__(attr)[1][3],
                obj.__getattribute__(attr)[2][0],
                obj.__getattribute__(attr)[2][1],
                obj.__getattribute__(attr)[2][2],
                obj.__getattribute__(attr)[2][3],
                obj.__getattribute__(attr)[3][0],
                obj.__getattribute__(attr)[3][1],
                obj.__getattribute__(attr)[3][2],
                obj.__getattribute__(attr)[3][3])

    @classmethod
    def set(cls, obj, attr, args):
        obj.__setattr__(attr, (args[0:4],args[4:8],args[8:12],args[12:16]))

#
# OSC RequestHandler
#

class BaseRequestHandler():
    @classmethod
    def _get_instance(cls, path, args):
        raise TypeError("not allowed to call this method from base class")

    @classmethod
    def _parse_instance(cls, args):
        raise TypeError("not allowed to call this method from base class")

    @classmethod
    def _parse_data(cls, args):
        raise TypeError("not allowed to call this method from base class")

    @classmethod
    def _reply(cls, typehandler, path, args, types, source, user_data):
        obj, attr = cls._get_instance(path, args)
        data = typehandler.get(obj, attr)
        target = cls._parse_instance(args)
        msg = Message(path)
        if target:
            msg.add(*target)
        if data:
            msg.add(*data)
        bge.logic.server.send(source.url, msg)

    @classmethod
    def _setvalue(cls, typehandler, path, args, types, source, user_data):
        obj, attr = cls._get_instance(path, args)
        data = cls._parse_data(args)
        typehandler.set(obj, attr, data)

    @classmethod
    def _method(cls, path, args, types, source, user_data):
        obj, attr = cls._get_instance(path, args)
        data = cls._parse_data(args)
        if data:
            return obj.__getattribute__(attr)(*data)
        else:
            return obj.__getattribute__(attr)()

    @classmethod
    def _method_reply(cls, path, source, target, data):
        msg = Message(path)
        msg.add(*target)
        msg.add(*data)
        bge.logic.server.send(source.url, msg)

# Reply Handler

    @classmethod
    def reply_bool(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeBool, path, args, types, source, user_data)

    @classmethod
    def reply_names(cls, path, args, types, source, user_data):
        cls._reply(AttributeNames, path, args, types, source, user_data)

    @classmethod
    def reply_string(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeString, path, args, types, source, user_data)

    @classmethod
    def reply_int(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeInt, path, args, types, source, user_data)

    @classmethod
    def reply_float(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeFloat, path, args, types, source, user_data)

    @classmethod
    def reply_vec3(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeVec3, path, args, types, source, user_data)

    @classmethod
    def reply_vec4(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeVec4, path, args, types, source, user_data)

    @classmethod
    def reply_matrix3x3(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeMatrix3x3, path, args, types, source, user_data)

    @classmethod
    def reply_matrix4x4(cls, path, args, types, source, user_data):
        cls._reply(AttributeTypeMatrix4x4, path, args, types, source, user_data)

# Set Value Handler
    @classmethod
    def set_bool_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeBool, path, args, types, source, user_data)

    @classmethod
    def set_string_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeString, path, args, types, source, user_data)

    @classmethod
    def set_int_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeInt, path, args, types, source, user_data)

    @classmethod
    def set_float_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeFloat, path, args, types, source, user_data)

    @classmethod
    def set_vec3_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeVec3, path, args, types, source, user_data)

    @classmethod
    def set_vec4_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeVec4, path, args, types, source, user_data)

    @classmethod
    def set_matrix3x3_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeMatrix3x3, path, args, types, source, user_data)

    @classmethod
    def set_matrix4x4_value(cls, path, args, types, source, user_data):
        cls._setvalue(AttributeTypeMatrix4x4, path, args, types, source, user_data)

# Method Handler
# naming convention:
# call_method => no param conversion, no return value
# call_method_reply => no param conversion, return non iterable type (numbers)
# call_method_reply_bool[vec3,...] => no param conversion, return type that need a conversion (e.g. vec3 to fff)
# custom handler defined in RequestHandler classes should look like this:
# call_method_[fmt]_reply_[return type]
# example: call_method_sfffx_reply_none (param: sfff, sfffi, sfffii, ...; returns nothing)
    @classmethod
    def call_method(cls, path, args, types, source, user_data):
        cls._method(path, args, types, source, user_data)

    @classmethod
    def call_method_reply(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, [value])

    @classmethod
    def call_method_reply_names(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        if not value is None:
            cls._method_reply(path, source, target, [", ".join([i.name for i in value])])
        else:
            cls._method_reply(path, source, target, [''])

    @classmethod
    def call_method_reply_name(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        if not value is None:
            cls._method_reply(path, source, target, [value.name])
        else:
            cls._method_reply(path, source, target, [''])

    @classmethod
    def call_method_reply_string(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        if not value is None:
            cls._method_reply(path, source, target, [str(value)])
        else:
            cls._method_reply(path, source, target, [''])

    @classmethod
    def call_method_reply_bool(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, [int(value)])

    @classmethod
    def call_method_reply_vec2(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, value)

    @classmethod
    def call_method_reply_vec3(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, value)

    @classmethod
    def call_method_reply_vec4(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, value)

    @classmethod
    def call_method_reply_matrix3x3(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, value)

    @classmethod
    def call_method_reply_matrix4x4(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, value)

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

class CameraRequestHandler(BaseRequestHandler):
    @classmethod
    def _get_instance(cls, path, args):
        sc = bge.logic.getCurrentScene()
        attr = path.split('/')[-1:][0]
        if args[0] in sc.cameras:
            return (sc.cameras[args[0]], attr)
        else:
            raise ValueError

    @classmethod
    def _parse_instance(cls, args):
        return args[:1]

    @classmethod
    def _parse_data(cls, args):
        return args[1:]

    @classmethod
    def call_method_sfffx_reply(cls, path, args, types, source, user_data):
        nargs = [args[0], (args[1],args[2],args[3])]
        for i in args[4:]:
            nargs.append(i)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_s24f_reply(cls, path, args, types, source, user_data):
        nargs = [args[0]]
        box = [[nargs[i*3+1], nargs[i*3+2], nargs[i*3+3]] for i in range(8)]
        nargs.append(box)
        cls.call_method_reply(path, nargs, types, source, user_data)

    @classmethod
    def call_method_siiii_reply_none(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method(path, nargs, types, source, user_data)

    @classmethod
    def call_method_ss_reply_vec2(cls, path, args, types, source, user_data):
        nargs = [args[0], bge.logic.getCurrentScene().objects[args[1]]]
        cls.call_method_reply_vec2(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sfff_reply_vec2(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method_reply_vec2(path, nargs, types, source, user_data)

    @classmethod
    def call_method_sff_reply_vec3(cls, path, args, types, source, user_data):
        nargs = [args[0], nargs[1:]]
        cls.call_method_reply_vec3(path, nargs, types, source, user_data)

class LibloServer(Server):
    def __init__(self, port, proto=UDP):
        super().__init__(port, proto)
        self.clients = set()

        # TODO: projection matrix stored in blendfile is not used on startup
        #       it needs to be set after connecting with first client
        self.init = False

        self.add_method("/connect", '', self.cb_connect)
        self.add_method("/shutdown", '', self.cb_shutdown)

        # Handler for KX_Scene

        self.add_method("/scene/name", "", SceneRequestHandler.reply_string)
        self.add_method("/scene/objects", "", SceneRequestHandler.reply_names)
        self.add_method("/scene/objectsInactive", "", SceneRequestHandler.reply_names)
        self.add_method("/scene/lights", "", SceneRequestHandler.reply_names)
        self.add_method("/scene/cameras", "", SceneRequestHandler.reply_names)
        self.add_method("/scene/active_camera", "", SceneRequestHandler.reply_string)

        self.add_method("/scene/suspended", "", SceneRequestHandler.reply_bool)
        self.add_method("/scene/activity_culling", "", SceneRequestHandler.reply_bool)

        self.add_method("/scene/activity_culling_radius", "", SceneRequestHandler.reply_float)
        self.add_method("/scene/activity_culling_radius", "f", SceneRequestHandler.set_float_value)

        self.add_method("/scene/dbvt_culling", "", SceneRequestHandler.reply_bool)

        self.add_method("/scene/pre_draw", "", SceneRequestHandler.reply_names)
        self.add_method("/scene/post_draw", "", SceneRequestHandler.reply_names)

        self.add_method("/scene/gravity", "", SceneRequestHandler.reply_vec3)
        self.add_method("/scene/gravity", "fff", SceneRequestHandler.set_vec3_value)

        self.add_method("/scene/addObject", "ss", SceneRequestHandler.call_method)
        self.add_method("/scene/addObject", "ssi", SceneRequestHandler.call_method)

        self.add_method("/scene/end", "", SceneRequestHandler.call_method)
        self.add_method("/scene/restart", "", SceneRequestHandler.call_method)
        self.add_method("/scene/replace", "s", SceneRequestHandler.call_method)
        self.add_method("/scene/suspend", "", SceneRequestHandler.call_method)
        self.add_method("/scene/resume", "", SceneRequestHandler.call_method)
        self.add_method("/scene/drawObstacleSimulation", "", SceneRequestHandler.call_method)

        # Handler for KX_GameObject

        self.add_method("/scene/objects/name", "s", GameObjectRequestHandler.reply_string)

        self.add_method("/scene/objects/mass", "sf", GameObjectRequestHandler.set_float_value)
        self.add_method("/scene/objects/mass", "s", GameObjectRequestHandler.reply_float)

        self.add_method("/scene/objects/linVelocityMin", "sf", GameObjectRequestHandler.set_float_value)
        self.add_method("/scene/objects/linVelocityMin", "s", GameObjectRequestHandler.reply_float)

        self.add_method("/scene/objects/linVelocityMax", "sf", GameObjectRequestHandler.set_float_value)
        self.add_method("/scene/objects/linVelocityMax", "s", GameObjectRequestHandler.reply_float)

        self.add_method("/scene/objects/localInertia", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/parent", "s", GameObjectRequestHandler.reply_string)

        self.add_method("/scene/objects/groupMembers", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/groupObject", "s", GameObjectRequestHandler.reply_string)

        self.add_method("/scene/objects/scene", "s", GameObjectRequestHandler.reply_string)

        self.add_method("/scene/objects/visible", "si", GameObjectRequestHandler.set_bool_value)
        self.add_method("/scene/objects/visible", "s", GameObjectRequestHandler.reply_bool)

        self.add_method("/scene/objects/color", "sffff", GameObjectRequestHandler.set_vec4_value)
        self.add_method("/scene/objects/color", "s", GameObjectRequestHandler.reply_vec4)

        self.add_method("/scene/objects/occlusion", "si", GameObjectRequestHandler.set_bool_value)
        self.add_method("/scene/objects/occlusion", "s", GameObjectRequestHandler.reply_bool)

        self.add_method("/scene/objects/position", "s", GameObjectRequestHandler.reply_vec3)
        self.add_method("/scene/objects/position", "sfff", GameObjectRequestHandler.set_vec3_value)

        self.add_method("/scene/objects/orientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/orientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        self.add_method("/scene/objects/scaling", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/scaling", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/localOrientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/localOrientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        self.add_method("/scene/objects/worldOrientation", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/worldOrientation", "s", GameObjectRequestHandler.reply_matrix3x3)

        self.add_method("/scene/objects/localScale", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/localScale", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/worldScale", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/worldScale", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/localPosition", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/localPosition", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/worldPosition", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/worldPosition", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/localTransform", "sfff", GameObjectRequestHandler.set_matrix4x4_value)
        self.add_method("/scene/objects/localTransform", "s", GameObjectRequestHandler.reply_matrix4x4)

        self.add_method("/scene/objects/worldTransform", "sfff", GameObjectRequestHandler.set_matrix4x4_value)
        self.add_method("/scene/objects/worldTransform", "s", GameObjectRequestHandler.reply_matrix4x4)

        self.add_method("/scene/objects/localLinearVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/localLinearVelocity", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/worldLinearVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/worldLinearVelocity", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/localAngularVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/localAngularVelocity", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/worldAngularVelocity", "sfff", GameObjectRequestHandler.set_vec3_value)
        self.add_method("/scene/objects/worldAngularVelocity", "s", GameObjectRequestHandler.reply_vec3)

        self.add_method("/scene/objects/timeOffset", "sf", GameObjectRequestHandler.set_float_value)
        self.add_method("/scene/objects/timeOffset", "s", GameObjectRequestHandler.reply_float)

        self.add_method("/scene/objects/state", "si", GameObjectRequestHandler.set_int_value)
        self.add_method("/scene/objects/state", "s", GameObjectRequestHandler.reply_int)

        self.add_method("/scene/objects/meshes", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/sensors", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/controllers", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/actuators", "s", GameObjectRequestHandler.reply_names)

        #TODO
        #self.add_method("/scene/objects/attrDict", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/children", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/childrenRecursive", "s", GameObjectRequestHandler.reply_names)

        self.add_method("/scene/objects/life", "sf", GameObjectRequestHandler.set_float_value)
        self.add_method("/scene/objects/life", "s", GameObjectRequestHandler.reply_float)

        self.add_method("/scene/objects/endObject", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/replaceMesh", "ssii", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/setOcclusion", "sii", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/alignAxisToVect", "sfffif", GameObjectRequestHandler.call_alignAxisToVect)

        self.add_method("/scene/objects/getAxisVect", "sfff", GameObjectRequestHandler.call_getAxisVect)

        self.add_method("/scene/objects/applyMovement", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/applyMovement", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/applyRotation", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/applyRotation", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/applyForce", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/applyForce", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/applyTorque", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/applyTorque", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/getLinearVelocity", "si", GameObjectRequestHandler.call_method_reply_vec3)
        self.add_method("/scene/objects/getLinearVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        self.add_method("/scene/objects/setLinearVelocity", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/setLinearVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/getAngularVelocity", "si", GameObjectRequestHandler.call_method_reply_vec3)
        self.add_method("/scene/objects/getAngularVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        self.add_method("/scene/objects/setAngularVelocity", "sfffi", GameObjectRequestHandler.call_method_sfffx_reply_none)
        self.add_method("/scene/objects/setAngularVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_none)

        self.add_method("/scene/objects/getVelocity", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_vec3)
        self.add_method("/scene/objects/getVelocity", "s", GameObjectRequestHandler.call_method_reply_vec3)

        self.add_method("/scene/objects/getReactionForce", "s", GameObjectRequestHandler.call_method_reply_vec3)

        self.add_method("/scene/objects/applyImpulse", "sffffff", GameObjectRequestHandler.call_method_sffffff_reply_none)

        self.add_method("/scene/objects/suspendDynamics", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/restoreDynamics", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/enableRigidBody", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/disableRigidBody", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/setParent", "ssii", GameObjectRequestHandler.call_method_ssx_reply_none)
        self.add_method("/scene/objects/setParent", "ssi", GameObjectRequestHandler.call_method_ssx_reply_none)
        self.add_method("/scene/objects/setParent", "ss", GameObjectRequestHandler.call_method_ssx_reply_none)

        self.add_method("/scene/objects/removeParent", "s", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/getPhysicsId", "s", GameObjectRequestHandler.call_method_reply)

        self.add_method("/scene/objects/getPropertyNames", "s", GameObjectRequestHandler.call_method_reply_names)

        self.add_method("/scene/objects/getDistanceTo", "ss", GameObjectRequestHandler.call_method_ssx_reply_f)
        self.add_method("/scene/objects/getDistanceTo", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_f)

        self.add_method("/scene/objects/getVectTo", "ss", GameObjectRequestHandler.call_method_ssx_reply_vec3)
        self.add_method("/scene/objects/getVectTo", "sfff", GameObjectRequestHandler.call_method_sfffx_reply_vec3)

        self.add_method("/scene/objects/rayCastTo", "ssfs", GameObjectRequestHandler.call_method_ssx_reply_string)
        self.add_method("/scene/objects/rayCastTo", "sffffs", GameObjectRequestHandler.call_method_sfffx_reply_string)

# TODO: /scene/objects/rayCast
#       self.add_method("/scene/objects/rayCast", "ssffffsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)
#       self.add_method("/scene/objects/rayCast", "sfffsfsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)
#       self.add_method("/scene/objects/rayCast", "sfffffffsiii", GameObjectRequestHandler.call_method_sfffx_reply_string)

        self.add_method("/scene/objects/setCollisionMargin", "sf", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/sendMessage", "ssss", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/reinstancePhysicsMesh", "sss", GameObjectRequestHandler.call_method_reply_bool)

        self.add_method("/scene/objects/playAction", "sff", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffi", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffii", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffiif", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffiifi", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffiifif", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "sffiififi", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/playAction", "s", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/playAction", "si", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/getActionFrame", "si", GameObjectRequestHandler.call_method_reply)
        self.add_method("/scene/objects/getActionFrame", "s", GameObjectRequestHandler.call_method_reply)

        self.add_method("/scene/objects/setActionFrame", "sif", GameObjectRequestHandler.call_method)
        self.add_method("/scene/objects/setActionFrame", "si", GameObjectRequestHandler.call_method)

        self.add_method("/scene/objects/isPlayingAction", "si", GameObjectRequestHandler.call_method_reply_bool)
        self.add_method("/scene/objects/isPlayingAction", "s", GameObjectRequestHandler.call_method_reply_bool)

        # Handler for KX_Camera

        self.add_method("/scene/cameras/lens", "sf", CameraRequestHandler.set_float_value)
        self.add_method("/scene/cameras/lens", "s", CameraRequestHandler.reply_float)

        self.add_method("/scene/cameras/ortho_scale", "sf", CameraRequestHandler.set_float_value)
        self.add_method("/scene/cameras/ortho_scale", "s", CameraRequestHandler.reply_float)

        self.add_method("/scene/cameras/near", "sf", CameraRequestHandler.set_float_value)
        self.add_method("/scene/cameras/near", "s", CameraRequestHandler.reply_float)

        self.add_method("/scene/cameras/far", "sf", CameraRequestHandler.set_float_value)
        self.add_method("/scene/cameras/far", "s", CameraRequestHandler.reply_float)

        self.add_method("/scene/cameras/perspective", "si", CameraRequestHandler.set_bool_value)
        self.add_method("/scene/cameras/perspective", "s", CameraRequestHandler.reply_bool)

        self.add_method("/scene/cameras/frustum_culling", "si", CameraRequestHandler.set_bool_value)
        self.add_method("/scene/cameras/frustum_culling", "s", CameraRequestHandler.reply_bool)

        self.add_method("/scene/cameras/projection_matrix", "sffffffffffffffff", CameraRequestHandler.set_matrix4x4_value)
        self.add_method("/scene/cameras/projection_matrix", "s", CameraRequestHandler.reply_matrix4x4)

        self.add_method("/scene/cameras/model_matrix", "s", CameraRequestHandler.reply_matrix4x4)

        self.add_method("/scene/cameras/camera_to_world", "s", CameraRequestHandler.reply_matrix4x4)

        self.add_method("/scene/cameras/world_to_camera", "s", CameraRequestHandler.reply_matrix4x4)

        self.add_method("/scene/cameras/use_viewport", "si", CameraRequestHandler.set_bool_value)
        self.add_method("/scene/cameras/use_viewport", "s", CameraRequestHandler.reply_bool)

        self.add_method("/scene/cameras/sphereInsideFrustum", "sffff", CameraRequestHandler.call_method_sfffx_reply)

        self.add_method("/scene/cameras/boxInsideFrustum", "sffffffffffffffffffffffff", CameraRequestHandler.call_method_s24f_reply)

        self.add_method("/scene/cameras/pointInsideFrustum", "sfff", CameraRequestHandler.call_method_sfffx_reply)

        self.add_method("/scene/cameras/getCameraToWorld", "s", CameraRequestHandler.call_method_reply_matrix4x4)

        self.add_method("/scene/cameras/getWorldToCamera", "s", CameraRequestHandler.call_method_reply_matrix4x4)

        self.add_method("/scene/cameras/setOnTop", "s", CameraRequestHandler.call_method)

        self.add_method("/scene/cameras/setViewport", "siiii", CameraRequestHandler.call_method_siiii_reply_none)

        self.add_method("/scene/cameras/getScreenPosition", "ss", CameraRequestHandler.call_method_ss_reply_vec2)
        self.add_method("/scene/cameras/getScreenPosition", "sfff", CameraRequestHandler.call_method_sfff_reply_vec2)

        self.add_method("/scene/cameras/getScreenVect", "sff", CameraRequestHandler.call_method_sff_reply_vec3)

        self.add_method("/scene/cameras/getScreenRay", "sfffs", CameraRequestHandler.call_method_reply_name)


        self.add_method(None, None, self.cb_fallback)

    def cb_connect(self, path, args, types, source, user_data):
        print("SERVER: received client connect: ", source.url)
        self.clients.add(source.url)
        self.send(source.url, "/srvinfo", self.url)

    def cb_fallback(self, path, args, types, source, user_data):
        print ("SERVER_ received message: ", path, args, types, source.url, user_data)
        self.send(source.url, "/error", "unknown message")

    def cb_shutdown(self, path, args, types, source, user_data):
        print("SERVER: Shutting down")
        for i in self.clients:
            self.send(i, "/shutdown", source.url)
        bge.logic.endGame()
