import bpy
from . import client

##################################################################
#
#    Type Defs for Timeline Actions
#
##################################################################

ACTION_TYPE_ENUM = [("ActionDummy","Dummy","Dummy Action"), \
			 		("ActionVideoOpen","Open Video","Open a Video"), \
			 		("ActionCameraOpen","Connect Camera","Connect a Camera"), \
			 		("ActionVideoState","Set Video State","Set Play, Pause, Stop")]

def ACTION_TYPE_NAME(self, _type):
	types = [ i[0] for i in ACTION_TYPE_ENUM ]
	return ACTION_TYPE_ENUM[types.index(_type)][1]

def ACTION_TYPE_DESCRIPTION(_type):
	types = [ i[0] for i in ACTION_TYPE_ENUM ]
	return ACTION_TYPE_ENUM[types.index(_type)][2]

class TimelineActionDummy(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# action type definded in ACTION_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # action is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # action is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/debug")

	m_msg = bpy.props.StringProperty(default="Dummy Action")

	def send(self):
		client.client().send(self.m_oscpath, self.m_msg)

bpy.utils.register_class(TimelineActionDummy)

class TimelineActionVideoOpen(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# action type definded in ACTION_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # action is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # action is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/movie")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()

	def send(self):
		print("play movie")
		filepath = bpy.path.abspath(self.m_filepath)
		client.client().send(self.m_oscpath, self.m_object, self.m_image, filepath)

bpy.utils.register_class(TimelineActionVideoOpen)

class TimelineActionCameraOpen(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# action type definded in ACTION_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # action is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # action is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/camera")

	m_object = bpy.props.StringProperty()
	m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	m_image = bpy.props.StringProperty()

	def send(self):
#		filepath = bpy.path.abspath(self.m_filepath)
		print("connect camera")
		client.client().send(self.m_oscpath, self.m_object, self.m_image, self.m_filepath)

bpy.utils.register_class(TimelineActionCameraOpen)

class TimelineActionVideoState(bpy.types.PropertyGroup):
	m_marker = bpy.props.StringProperty()	# marker name (back ref to queue / timeline marker)
	m_type = bpy.props.StringProperty()		# action type definded in ACTION_TYPE_ENUM
	m_applied = bpy.props.BoolProperty(default=False) # action is applied (used in ui)
	m_hidden = bpy.props.BoolProperty(default=False) # action is hidden in ui
	m_oscpath = bpy.props.StringProperty(default="/texture/state")

	m_image = bpy.props.StringProperty()
	m_state = bpy.props.EnumProperty(
		items = [("PLAY","play","play Video"),
				("PAUSE","pause","pause Video"), 
				("STOP","stop","stop Video")],
		name = "state")

	def send(self):
		client.client().send(self.m_oscpath, self.m_image, self.m_state)
		
bpy.utils.register_class(TimelineActionVideoState)

class TimelineActions(bpy.types.PropertyGroup):
	'''
		Property Group that holds all Actions, sorted by types
	'''
	
	#TODO: use keys instead of ACTION_TYPE_ENUM

	ActionDummy = bpy.props.CollectionProperty(type=TimelineActionDummy)
	ActionVideoOpen = bpy.props.CollectionProperty(type=TimelineActionVideoOpen)
	ActionCameraOpen = bpy.props.CollectionProperty(type=TimelineActionCameraOpen)
	ActionVideoState = bpy.props.CollectionProperty(type=TimelineActionVideoState)
	
	m_types = bpy.props.EnumProperty(items = ACTION_TYPE_ENUM, name = "state")

    
#    def __get_idx(self):
#        return list(bpy.context.scene.yabee_settings.opt_anim_list.anim_collection).index(self)
#        
#    index = property(__get_idx)


	def add(self, _type):
		'''
			add a new action to the Actioncollections
		'''
		for info in ACTION_TYPE_ENUM:
			if _type == info[0]:
				entry = getattr(self, info[0]).add()
				entry.m_type = info[0]
				entry.m_hidden = False
				entry.m_applied = False
				
				# search for a unique name
				def check_name(collection, name, num):
					if "{0}.{1}".format(name, str(num).zfill(3)) in collection:
						return check_name(collection, name, num+1)
					return num

				num = check_name(getattr(self, info[0]), info[0], 1)
				entry.name = "{0}.{1}".format(info[0], str(num).zfill(3))
				print("test add: ", entry.name)

				return entry

	def remove(self, name):
		'''
			removes an action ()
		'''
		print("TimelineActions.remove: ", name)
		def get_type(name):
			for i in ACTION_TYPE_ENUM:
				if i[0] == name[:-4]:
					return i[0]

		_type = get_type(name)

		if not _type in self.keys():
			raise TypeError("requested type not found in timeline actions")

		collection = getattr(self, _type)

		if not name in collection:
			raise IndexError("requested action name not found in timeline actions")

		idx = collection.keys().index(name)
		collection.remove(idx)			

	def lookup(self, _name):
		def get_type(_name):
			for i in ACTION_TYPE_ENUM:
				if i[0] == _name[:-4]:
					return i[0]

		_type = get_type(_name)

		if not _type in self.keys():
			raise TypeError("requested type not found in timeline actions")

		collection = getattr(self, _type)

		if not _name in collection:
			raise IndexError("requested action name not found in timeline actions")

		return collection[_name]

bpy.utils.register_class(TimelineActions)

class TimelineQueueEntry(bpy.types.PropertyGroup):
	'''
		PropertyGroup for Action Queue Entries, references diff type of Actions
	'''
	m_marker = bpy.props.StringProperty()	# name of the queue id
	m_type = bpy.props.StringProperty()		# action type	
	m_action = bpy.props.StringProperty() 	# action name

	def add_action(self, actiontype):
		'''
			add a new action
		'''
		action = bpy.context.scene.timeline_actions.add(actiontype)
		self.m_action = action.name
		self.m_type = action.m_type
		return action

	def del_action(self):
		'''
			delete referenced action
		'''
		print("TimelineQueueEntry.del_action: ", self.m_marker, self.m_type, self.m_action)
		bpy.context.scene.timeline_actions.remove(self.m_action)

	def trigger(self):
		bpy.context.scene.timeline_actions.lookup(self.m_action).send()

bpy.utils.register_class(TimelineQueueEntry)

class TimelineQueue(bpy.types.PropertyGroup):
	'''
		PropertyGroup of Action Queues, stores Entries with Actions
	'''
	m_items = bpy.props.CollectionProperty(type=TimelineQueueEntry)
	m_execute_after = bpy.props.BoolProperty(default=False)
	m_pause = bpy.props.BoolProperty(default=True)

bpy.utils.register_class(TimelineQueue)


##################################################################
#
#    init Instances
#
##################################################################

bpy.types.Scene.timeline_actions = bpy.props.PointerProperty(type=TimelineActions, options={"HIDDEN"})
bpy.types.Scene.timeline_queues = bpy.props.CollectionProperty(type=TimelineQueue, options={"HIDDEN"})

bpy.types.Scene.active_marker = bpy.props.IntProperty(options={"HIDDEN"}, subtype='UNSIGNED')
bpy.types.Scene.active_queues_entry = bpy.props.StringProperty(options={"HIDDEN"})

##################################################################
#
#    Operators
#
##################################################################

#
#    Operator to add new Timeline Actions 
#
class BLive_OT_action_add(bpy.types.Operator):
	'''
		adds a new action to action queue and extends TimelineAction
		with properties based on requested action type
	'''
	bl_idname = "blive.action_add"
	bl_label = "BLive add timeline action"
	
	type = bpy.props.EnumProperty(items = ACTION_TYPE_ENUM, name = "type")

	def execute(self, context):
		if len(context.scene.timeline_markers):
			queue_name = context.scene.timeline_markers[context.scene.active_marker].name
			
			# query action type from ACTION_TYPE_ENUM
			action_prefix = None
			for i in ACTION_TYPE_ENUM:
				if i[0] == self.type:
					action_prefix = i[0]
			if not action_prefix:
				print('blive.action_add - cancelled')
				return{'CANCELLED'}
			
			# add new queue
			if not queue_name in context.scene.timeline_queues:
				queue = bpy.context.scene.timeline_queues.add()
				queue.name = queue_name
			
			# add new action entry to queue
			queue = bpy.context.scene.timeline_queues[queue_name]
			item = queue.m_items.add()
			action = item.add_action(action_prefix)
			item.name = action.name

		return{'FINISHED'}
		
class BLive_OT_queue_add(bpy.types.Operator):
	'''
		adds a action queue
	'''
	bl_idname = "blive.queue_add"
	bl_label = "BLive add timeline queue"
	
	def execute(self, context):	
		queue_name = context.scene.timeline_markers[context.scene.active_marker].name

		if not queue_name in context.scene.timeline_queues:
			queue = bpy.context.scene.timeline_queues.add()
			queue.name = queue_name
			return{'FINISHED'}
		else:
			return{'CANCELLED'}
			
class BLive_OT_action_delete(bpy.types.Operator):
	'''
		Delete Action
	'''
	bl_idname = "blive.action_delete"
	bl_label = "BLive delete timeline action"
	m_action = bpy.props.StringProperty()
	
	def execute(self, context):
		marker = context.scene.active_marker
		idx = context.scene.timeline_queues[marker].m_items.keys().index(self.m_action)
		context.scene.timeline_queues[marker].m_items[idx].del_action()
		context.scene.timeline_queues[marker].m_items.remove(idx)
		return{'FINISHED'}

class BLive_OT_dummy(bpy.types.Operator):
	'''
		Dummy Operator
	'''
	bl_idname = "blive.dummy"
	bl_label = "BLive Dummy Operator"
	msg = bpy.props.StringProperty(default="")
	
	def execute(self, context):
		print("Dummy Operator: ", self.msg)
		return{'FINISHED'}

#
#    BLive Timeline Marker List located in NLA Editor UI region
#
class BLive_PT_timeline_marker(bpy.types.Panel):
	bl_label = "BLive Timeline Marker"
	bl_space_type = "NLA_EDITOR"
	bl_region_type = "UI"
	
	@classmethod
	def poll(self, context):
		return bool(len(context.scene.timeline_markers))

	def draw(self, context):
		layout = self.layout

		active_marker = context.scene.active_marker
		marker_id = context.scene.timeline_markers[active_marker].name

		#    list of timeline markers 
		scene = context.scene
		row = layout.row()
		row.template_list(scene, "timeline_markers", scene, "active_marker", rows=2, maxrows=2)

		#    add queue
		row = layout.row()
		row.operator("blive.queue_add", text="Add Queue")

		#    boxes for actions
		if marker_id in context.scene.timeline_queues:
		
			#	queue attr (pause, send after) 
			box = layout.box()
			row = box.row()
			row.prop(context.scene.timeline_queues[marker_id], "m_pause", text="pause")
			row.prop(context.scene.timeline_queues[marker_id], "m_execute_after", text="send after")
					
			#    menu to choose new action
			row = layout.row()
			row.operator_menu_enum("blive.action_add", "type", text="Add Action")

			for item in context.scene.timeline_queues[marker_id].m_items:	
				#    get action from queue entry
				action = context.scene.timeline_actions.lookup(item.m_action)

				main = layout.column(align=True)
				head = main.box()
				split = head.split(percentage=0.7)
				row = split.row()
				if action.m_hidden:
					row.prop(action, "m_hidden", text="", icon="TRIA_RIGHT", emboss=False)
				else:
					row.prop(action, "m_hidden", text="", icon="TRIA_DOWN", emboss=False)
				row.label( ACTION_TYPE_DESCRIPTION(item.m_type) )
				split = split.split(percentage=1)
				buttons = split.column_flow(columns=2, align=True)
				if not action.m_applied:
					buttons.prop(action, "m_applied", text="", icon="UNLOCKED", toggle=True)
				else:
					buttons.prop(action, "m_applied", text="", icon="LOCKED", toggle=True)

				buttons.operator("blive.action_delete", text="", icon="PANEL_CLOSE").m_action =  item.m_action

				if not action.m_hidden:
					body = main.box()
					try:
						getattr(self, item.m_type)(context, action, body)
					except:
						row = body.row()
						row.label("not implemented")

	def ActionVideoOpen(self, context, action, ui):
		if action.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(action, "m_filepath", text="Open File", icon="FILE_MOVIE")
		row = ui.row()
		row.prop(action, "m_object", text="Choose Object", icon="OBJECT_DATA")
		row = ui.row()
		row.prop(action, "m_image", text="Choose Image", icon="TEXTURE")

	def ActionCameraOpen(self, context, action, ui):
		if action.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(action, "m_filepath", text="Open File", icon="FILE_MOVIE")
		row = ui.row()
		row.prop(action, "m_object", text="Choose Object", icon="OBJECT_DATA")
		row = ui.row()
		row.prop(action, "m_image", text="Choose Image", icon="TEXTURE")
		
	def ActionVideoState(self, context, action, ui):
		if action.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(action, "m_state", text="")
		row = ui.row()
		row.prop(action, "m_image", text="Choose Image", icon="TEXTURE")

	def ActionDummy(self, context, action, ui):
		if action.m_applied:
			ui.enabled = False

		row = ui.row()
		row.prop(action, "m_msg", text="send Message")
		
def unregister():
	bpy.utils.unregister_module(__name__)
