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

import bpy
import math
import bmesh 
#from ..client import BLiveClient

# TODO: all calls defined as def outside the Operator to avoid the RuntimeError recursion

#def osc_object_location(ob):
	#BLiveClient().send("/data/object/location", [ob.name, ob.location[0], ob.location[1], ob.location[2]])

#class BLive_OT_osc_object_location(bpy.types.Operator):
	#"""
		#Operator - send object location
	#"""
	#bl_idname = "blive.osc_object_location"
	#bl_label = "BLive - send object location"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#ob = context.scene.objects[self.obname]
		#osc_object_location(ob)
		##~ BLiveClient().send("/data/object/location", [self.obname, ob.location[0], ob.location[1], ob.location[2]])
		#return{'FINISHED'} 

#def osc_object_rotation(ob):
	#BLiveClient().send("/data/object/rotation", [ob.name, ob.rotation_euler[0], ob.rotation_euler[1], ob.rotation_euler[2]])

#class BLive_OT_osc_object_rotation(bpy.types.Operator):
	#"""
		#Operator - send object rotation
	#"""
	#bl_idname = "blive.osc_object_rotation"
	#bl_label = "BLive - send object rotation"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#ob = context.scene.objects[self.obname]
		#osc_object_rotation(ob)
		##~ BLiveClient().send("/data/object/rotation", [self.obname, ob.rotation_euler[0], ob.rotation_euler[1], ob.rotation_euler[2]])
		#return{'FINISHED'} 

#def osc_object_scaling(ob):
	#BLiveClient().send("/data/object/scaling", [ob.name, ob.scale[0], ob.scale[1], ob.scale[2]])

#class BLive_OT_osc_object_scaling(bpy.types.Operator):
	#"""
		#Operator - send object scaling
	#"""
	#bl_idname = "blive.osc_object_scaling"
	#bl_label = "BLive - send object scaling"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#if self.obname in context.scene.objects and context.scene.objects[self.obname].type == 'MESH':
			#ob = context.scene.objects[self.obname]
			#osc_object_scaling(ob)
			##~ BLiveClient().send("/data/object/scaling", [self.obname, ob.scale[0], ob.scale[1], ob.scale[2]])
			#return{'FINISHED'} 
		#else:
			#return{'CANCELLED'}

#def osc_object_camera(camera):
	#perspective = 1
	#if camera.type == 'ORTHO':
		#perspective = 0
	#aspect = bpy.context.scene.game_settings.resolution_y/bpy.context.scene.game_settings.resolution_x
	#BLiveClient().send("/data/object/camera",[ camera.name, camera.angle, aspect, camera.ortho_scale, camera.clip_start, camera.clip_end, perspective, camera.shift_x, camera.shift_y])

#class BLive_OT_osc_object_camera(bpy.types.Operator):
	#"""
		#Operator - send camera data
	#"""
	#bl_idname = "blive.osc_object_camera"
	#bl_label = "BLive - send camera data"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#if self.obname in context.scene.objects and context.scene.objects[self.obname].type == 'CAMERA':
			#camera = bpy.data.cameras[self.obname]
			#osc_object_camera(camera)
			##~ perspective = 1
			##~ if camera.type == 'ORTHO':
				##~ perspective = 0
			##~ aspect = context.scene.game_settings.resolution_y/context.scene.game_settings.resolution_x
			##~ BLiveClient().send("/data/object/camera",[ self.obname, camera.angle, aspect, camera.ortho_scale, camera.clip_start, camera.clip_end, perspective, camera.shift_x, camera.shift_y])
			#return{'FINISHED'} 
		#else:
			#return{'CANCELLED'}

#def osc_object_lamp(lamp):
	#BLiveClient().send("/data/object/lamp", [lamp.name, lamp.energy, lamp.color[0], lamp.color[1], lamp.color[2]])
	#if lamp.type == 'POINT':
		#BLiveClient().send("/data/object/lamp/normal", [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation])
	#elif lamp.type == 'SPOT':
		#BLiveClient().send("/data/object/lamp/spot",  [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation, math.degrees(lamp.spot_size), lamp.spot_blend])
	#elif lamp.type == 'SUN':
		#BLiveClient().send("/data/object/lamp/sun", [lamp.name])

#class BLive_OT_osc_object_lamp(bpy.types.Operator):
	#"""
		#Operator - send lamp data
	#"""
	#bl_idname = "blive.osc_object_lamp"
	#bl_label = "BLive - send lamp data"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#if self.obname in context.scene.objects and context.scene.objects[self.obname].type == 'LAMP':
			#lamp = context.scene.objects[self.obname]
			#osc_object_lamp(lamp)
			##~ BLiveClient().send("/data/object/lamp", [lamp.name, lamp.energy, lamp.color[0], lamp.color[1], lamp.color[2]])
			##~ if lamp.type == 'POINT':
				##~ BLiveClient().send("/data/object/lamp/normal", [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation])
			##~ elif lamp.type == 'SPOT':
				##~ BLiveClient().send("/data/object/lamp/spot",  [lamp.name, lamp.distance,  lamp.linear_attenuation, lamp.quadratic_attenuation, lamp.spot_size, lamp.spot_blend])
			##~ elif lamp.type == 'SUN':
				##~ BLiveClient().send("/data/object/lamp/sun", [lamp.name])
			#return{'FINISHED'}
		#else:
			#return{'CANCELLED'}

#def osc_object_meshdata(ob):
	#mesh = bmesh.from_edit_mesh(ob.data)
	#for face in mesh.faces:
		#for vindex, vertex in enumerate(face.verts):
			#BLiveClient().send("/data/object/mesh", [ob.name, face.index, vindex, vertex.co[0], vertex.co[1], vertex.co[2]])

#class BLive_OT_osc_object_meshdata(bpy.types.Operator):
	#"""
		#Operator - send mesh data
	#"""
	#bl_idname = "blive.osc_object_meshdata"
	#bl_label = "BLive - send meshdata"
	#obname = bpy.props.StringProperty()

	#def execute(self, context):
		#if self.obname in context.scene.objects and context.scene.objects[self.obname].type == 'MESH':
			#ob = context.scene.objects[self.obname]
			#try:
				#osc_object_meshdata(ob)
				#return{'FINISHED'}
			#except ValueError as err:
				#print('Error on mesh update: ', err)
				#return{'CANCELLED'}

def register():
	print("object.ops.register")
	#bpy.utils.register_class(BLive_OT_osc_object_location)
	#bpy.utils.register_class(BLive_OT_osc_object_rotation)
	#bpy.utils.register_class(BLive_OT_osc_object_scaling)
	#bpy.utils.register_class(BLive_OT_osc_object_camera)
	#bpy.utils.register_class(BLive_OT_osc_object_lamp)
	#bpy.utils.register_class(BLive_OT_osc_object_meshdata)

def unregister():
	print("object.ops.unregister")
	#bpy.utils.unregister_class(BLive_OT_osc_object_location)
	#bpy.utils.unregister_class(BLive_OT_osc_object_rotation)
	#bpy.utils.unregister_class(BLive_OT_osc_object_scaling)
	#bpy.utils.unregister_class(BLive_OT_osc_object_camera)
	#bpy.utils.unregister_class(BLive_OT_osc_object_lamp)
	#bpy.utils.unregister_class(BLive_OT_osc_object_meshdata)
