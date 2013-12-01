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
import math
from liblo import Message

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

class AttributeName(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        if not obj.__getattribute__(attr):
            return [""]
        else:
            obj.__getattribute__(attr)

class AttributeNameList(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        if not obj.__getattribute__(attr):
            return [""]
        else:
            return [", ".join([i.name for i in obj.__getattribute__(attr)])]

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

class AttributeTypeVec4(AttributeType):
    @classmethod
    def get(cls, obj, attr):
        return [obj.__getattribute__(attr)[0],
                obj.__getattribute__(attr)[1],
                obj.__getattribute__(attr)[2],
                obj.__getattribute__(attr)[3]]

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
        obj.__setattr__(attr, (args[0:4],args[4:8],args[8:12],args[12:16]) )

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
    def reply_name(cls, path, args, types, source, user_data):
        cls._reply(AttributeName, path, args, types, source, user_data)

    @classmethod
    def reply_namelist(cls, path, args, types, source, user_data):
        cls._reply(AttributeNameList, path, args, types, source, user_data)

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

    #
    # Set Value Handler
    #
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
    #
    # Method Handler
    #
    @classmethod
    def call_method(cls, path, args, types, source, user_data):
        cls._method(path, args, types, source, user_data)

    @classmethod
    def call_method_reply(cls, path, args, types, source, user_data):
        value = cls._method(path, args, types, source, user_data)
        target = cls._parse_instance(args)
        cls._method_reply(path, source, target, [value])

    @classmethod
    def call_method_reply_namelist(cls, path, args, types, source, user_data):
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
    def call_method_reply_vec(cls, path, args, types, source, user_data):
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
