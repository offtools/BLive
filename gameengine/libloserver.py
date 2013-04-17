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
		return [str(obj.__getattribute__(attr))]

class AttributeObjectList(AttributeType):
	@classmethod
	def get(cls, obj, attr):
		return [i.name for i in obj.__getattribute__(attr)]

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
	def _method(cls, obj, attr, data):
		pass

# Reply Handler

	@classmethod
	def reply_bool(cls, path, args, types, source, user_data):
		cls._reply(AttributeTypeBool, path, args, types, source, user_data)

	@classmethod
	def reply_objectlist(cls, path, args, types, source, user_data):
		cls._reply(AttributeObjectList, path, args, types, source, user_data)

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
		print("reply_matrix3x3")
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
	@classmethod
	def call_method(cls, path, args, types, source, user_data):
		obj, attr = cls._get_instance(path, args)
		data = cls._parse_data(args)
		if data:
			ret = obj.__getattribute__(attr)(*data)
		else:
			ret = obj.__getattribute__(attr)()
		if ret:
			print("call_method - return value: ", ret)

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
			return (scene.objectsInactive[args[0]], attr)
		else:
			raise ValueError

	@classmethod
	def _parse_instance(cls, args):
		return args[:1]

	@classmethod
	def _parse_data(cls, args):
		return args[1:]

class LibloServer(Server):
	def __init__(self, port, proto=UDP):
		super().__init__(port, proto)
		self.clients = set()

		# all optional parameters needed


		# Handler for KX_Scene

		self.add_method("/scene/name", "", SceneRequestHandler.reply_string)
		self.add_method("/scene/objects", "", SceneRequestHandler.reply_objectlist)
		self.add_method("/scene/objectsInactive", "", SceneRequestHandler.reply_objectlist)
		self.add_method("/scene/lights", "", SceneRequestHandler.reply_objectlist)
		self.add_method("/scene/cameras", "", SceneRequestHandler.reply_objectlist)
		self.add_method("/scene/active_camera", "", SceneRequestHandler.reply_string)

		self.add_method("/scene/suspended", "", SceneRequestHandler.reply_bool)
		self.add_method("/scene/activity_culling", "", SceneRequestHandler.reply_bool)

		self.add_method("/scene/activity_culling_radius", "", SceneRequestHandler.reply_float)
		self.add_method("/scene/activity_culling_radius", "f", SceneRequestHandler.set_float_value)

		self.add_method("/scene/dbvt_culling", "", SceneRequestHandler.reply_bool)

		self.add_method("/scene/pre_draw", "", SceneRequestHandler.reply_objectlist)
		self.add_method("/scene/post_draw", "", SceneRequestHandler.reply_objectlist)

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

		self.add_method("/scene/objects/localInertia", "sfff", GameObjectRequestHandler.set_vec3_value)
		self.add_method("/scene/objects/localInertia", "s", GameObjectRequestHandler.reply_vec3)

		self.add_method("/scene/objects/parent", "s", GameObjectRequestHandler.reply_string)

		self.add_method("/scene/objects/groupMembers", "s", GameObjectRequestHandler.reply_objectlist)

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
		self.add_method("/scene/objects/orientation", "s", GameObjectRequestHandler.reply_vec3)

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

		self.add_method("/scene/objects/state", "sf", GameObjectRequestHandler.set_int_value)
		self.add_method("/scene/objects/state", "s", GameObjectRequestHandler.reply_int)

		self.add_method("/scene/objects/meshes", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/sensors", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/controllers", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/actuators", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/attrDict", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/children", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/childrenRecursive", "s", GameObjectRequestHandler.reply_objectlist)

		self.add_method("/scene/objects/life", "sf", GameObjectRequestHandler.set_float_value)
		self.add_method("/scene/objects/life", "s", GameObjectRequestHandler.reply_float)

		self.add_method("/scene/objects/endObject", "s", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/replaceMesh", "ssii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/setOcclusion", "sii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/setVisible", "sii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/alignAxisToVect", "sfffif", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/getAxisVect", "sfff", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/applyMovement", "sfffii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/applyRotation", "sfffii", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/applyForce", "sfffi", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/applyTorque", "sfffi", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/getLinearVelocity", "si", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/setLinearVelocity", "sfffi", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/getAngularVelocity", "si", GameObjectRequestHandler.call_method)

		self.add_method("/scene/objects/setAngularVelocity", "sfffi", GameObjectRequestHandler.call_method)

		self.add_method("/connect", '', self.cb_connect)
		self.add_method(None, None, self.cb_fallback)

	def cb_connect(self, path, args, types, source, user_data):
		print("SERVER: received client connect: ", source.url)
		self.clients.add(source.url)
		self.send(source.url, "/srvinfo", self.url)

	def cb_fallback(self, path, args, types, source, user_data):
		print ("SERVER_ received message: ", path, args, types, source.url, user_data)
		self.send(source.url, "/error", "unknown message")

	def stop(self):
		print("SERVER: Shutting down")
		for i in self.clients:
			self.send(i, "/shutdown", self.url)

def Init(port):
	if not hasattr(bge.logic, "server"):
		print("libloserver.INIT - port: ", port)
		bge.logic.server = LibloServer(port)
