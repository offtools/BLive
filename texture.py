import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty
from . import client

class BLive_OT_open_video_filebrowser(bpy.types.Operator):
	bl_idname = "blive.open_video_filebrowser"
	bl_label = "BLive Open Video Filebrowser"
	bl_options = {'REGISTER', 'UNDO'}
	
	filepath = StringProperty(subtype="FILE_PATH")
	filename = StringProperty()
	files = CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
	directory = StringProperty(subtype='DIR_PATH')
	use_filter_movie = BoolProperty(default=True)
	use_filter = BoolProperty(default=True)

	def execute(self, context):
		print(self.files, self.directory, self.filepath, self.filename)
		if "PORT" in bpy.context.scene.camera.game.properties:
			ob = bpy.context.object.name	
			tex = "IM{0}".format(bpy.context.object.active_material.active_texture.image.name)
			client.client().cmd_open_video(ob, tex, self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
        
bpy.utils.register_class(BLive_OT_open_video_filebrowser)

class BLive_PT_texture_player(bpy.types.Panel):
	bl_label = "BLive Videoplayer"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "texture"

	def draw(self, context):
		row = self.layout.row(align=True)
		try:
			row.label("Image: {0}".format(bpy.context.object.active_material.active_texture.image.name))
			row.operator("blive.open_video_filebrowser", text="Open", icon="FILE_MOVIE")

		except AttributeError:
			return
			
		row = self.layout.row(align=True)
		tex = bpy.context.object.active_material.active_texture
		row.template_image(tex, "image", tex.image_user, compact=True)
