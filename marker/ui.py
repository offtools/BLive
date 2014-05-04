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
#   Panel located in NLA Editor
#

# TODO: Error Handling for TriggerGameProperty

import bpy

class TRIGGER_UL_queues(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        queues = data
        queue = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(queue, 'name', text='', emboss=False)
            if queue.marker:
                layout.prop(queue, 'marker', icon='PMARKER_SEL', icon_only=True, emboss=False)
            else:
                layout.prop(queue, 'marker', icon='ERROR', icon_only=True, emboss=False)

        # TODO: 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(queue.name)

class BLive_PT_timeline_marker_trigger(bpy.types.Panel):
    bl_label = "BLive Timeline Marker Trigger"
    bl_space_type = "NLA_EDITOR"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        data = scene.timeline_marker_trigger.data
        queues= scene.timeline_marker_trigger.queues
        idx = context.scene.timeline_marker_trigger.active_queue

        # list Queues
        row = layout.row()
        if bpy.app.version[1] < 66:
            row.template_list(scene.timeline_marker_trigger, "queues", scene.timeline_marker_trigger, "active_queue", rows=1, maxrows=4)
        else:
            row.template_list("TRIGGER_UL_queues", "queues", scene.timeline_marker_trigger, "queues", scene.timeline_marker_trigger, "active_queue", rows=1, maxrows=4)
        col = row.column(align=True)
        col.operator('blive.timeline_trigger_add_queue', text='', icon='ZOOMIN')
        col.operator('blive.timeline_trigger_remove_queue', text='', icon='ZOOMOUT')

        if idx > -1 and idx < len(context.scene.timeline_marker_trigger.queues):
            queue = queues[scene.timeline_marker_trigger.active_queue]
            layout.label("Assign Timeline Marker")
            row = layout.row(align=True)
            row.prop_search(queue, 'marker', scene, 'timeline_markers', text="")
            row.operator("blive.timeline_trigger_add_assign_marker", text="", icon="ZOOMIN")
            row.operator("blive.timeline_trigger_remove_revoke_marker", text="", icon="ZOOMOUT")
            row = layout.row()
            row.prop(queue, "execute_after")
            row.prop(queue, "pause")

            # Trigger Slots
            layout.operator_menu_enum("blive.timeline_trigger_add_slot", "type", text="Add Trigger Slot")
            for slot in queue.queue_slots:
                frame = layout.column(align=True)
                header = frame.box()
                row = header.row()
                row.prop(slot, "show_all", text="", icon="TRIA_RIGHT", emboss=False)
                col = row.column()
                col.label(slot.name)
                col = row.column()
                col.operator("blive.timeline_trigger_remove_slot", text="", icon="PANEL_CLOSE").slot=slot.name
                if slot.show_all and slot.name in getattr(data, slot.type):
                    body = frame.box()
                    slot_data = getattr(data, slot.type)[slot.name]
                    getattr(self, slot.type)(context, slot_data, body)

    def TriggerOpenVideo(self, context, slot_data, layout):
        row = layout.row()
        row.prop(slot_data, "filepath")
        row = layout.row()
        row.prop_search(slot_data, "object", context.scene, "objects", text="Object")
        row = layout.row()
        row.prop_search(slot_data, "image", bpy.data, "images", text="Image")
        row = layout.row()
        row.prop(slot_data, "audio", text="enable Audio")
        if slot_data.audio:
            row = layout.row()
            row.prop(slot_data, "volume", text="Volume")
        row = layout.row()
        row.prop(slot_data, "loop", text="Loop Video")
        row = layout.row()
        row.prop(slot_data, "preseek", text="Preseek")
        row = layout.row(align=True)
        row.prop(slot_data, "inp", text="Inpoint")
        row.prop(slot_data, "outp", text="Outpoint")
        row = layout.row()
        row.prop(slot_data, "deinterlace", text="Deinterlace")

    def TriggerOpenCamera(self, context, slot_data, layout):
        row = layout.row()
        row.prop(slot_data, "device", text="Device")
        row = layout.row()
        row.prop_search(slot_data, "object", context.scene, "objects", text="Object")
        row = layout.row()
        row.prop_search(slot_data, "image", bpy.data, "images", text="Image")
        row = layout.row(align=True)
        row.prop(slot_data, "width", text="Width")
        row.prop(slot_data, "height", text="Height")
        row = layout.row()
        row.prop(slot_data, "rate", text="Rate")
        row = layout.row()
        row.prop(slot_data, "deinterlace", text="Deinterlace")

    def TriggerVideotextureState(self, context, slot_data, layout):
        row = layout.row()
        row.prop_search(slot_data, "image", bpy.data, "images", text="image")
        row = layout.row()
        row.prop(slot_data, "state", text="")

    def TriggerChangeScene(self, context, slot_data, layout):
        row = layout.row()
        row.prop_search(slot_data, "scene", context.blend_data, "scenes", text="Scene")

    def TriggerGameProperty(self, context, slot_data, layout):
        row = layout.row()
        row.prop_search(slot_data, "object", context.scene, "objects", text="Object")
        row = layout.row()
        row.prop(slot_data, "gameproperty", text="Game Property")

    def TriggerOSCMessage(self, context, slot_data, layout):
        row = layout.row()
        row.prop(slot_data, "msg", text="OSC Message")

    def TriggerScript(self, context, slot_data, layout):
        row = layout.row()
        row.prop_search(slot_data, "script", context.blend_data, "texts", text="Script")

#class BLive_PT_multitrack_cuelist(bpy.types.Panel):
    #bl_label = "BLive Multitrack Cuelist"
    #bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOLS"

    #@classmethod
    #def poll(self, context):
        #return True

    #def draw(self, context):
        #layout = self.layout
        #mtcl = context.window_manager.multitrack_cuelist
        #row = layout.row()
        #row.prop(mtcl, "active_page", text="Page")
        #row.prop(mtcl, "cols_per_page", text="Tacks per Page")
        #row.operator("blive.mtcl_add_column", text="Add Column")
        #row.operator("blive.mtcl_add_cue", text="Add Cue")

        #for i in range(len(mtcl.cues)):
            #row = layout.row()
            #row.label(mtcl.cues[i].name)
            #for col in mtcl.columns:
                #col = row.column()
                #col.label(col, "image")


def register():
    print("marker.ui.register")
    bpy.utils.register_class(TRIGGER_UL_queues)
    bpy.utils.register_class(BLive_PT_timeline_marker_trigger)
    #bpy.utils.register_class(BLive_PT_multitrack_cuelist)

def unregister():
    print("marker.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_timeline_marker_trigger)
    bpy.utils.unregister_class(TRIGGER_UL_queues)
    #bpy.utils.unregister_class(BLive_PT_multitrack_cuelist)
