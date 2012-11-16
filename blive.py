import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, EnumProperty

class BLiveSettings(bpy.types.PropertyGroup):
	pass

#	temporary data, no need to store into blend file (reset on load)
class BLiveTmp(bpy.types.PropertyGroup):
	modal_mesh_edit = EnumProperty(default=False, options={"HIDDEN"})
	active_marker = bpy.props.IntProperty(options={"HIDDEN"}, subtype='UNSIGNED')

def init():
	#	1. declare data structures (Properties)
	#	timeline trigger, queues
	#	window_manager.modal_mesh_updater
	
	#	2. instance data structures
	#	active marker, active queue
	#	window_manager.modal_mesh_updater
	
	#	3. add handlers
	bpy.app.handlers.frame_change_pre.append(__frame_change_pre_handler)
	bpy.app.handlers.scene_update_post.append(__scene_update_post_handler)
	
	#	4. register operators and ui elements
