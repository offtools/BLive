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

class BLive_PT_timeline_trigger(bpy.types.Panel):
    bl_label = "BLive Timeline Trigger"
    bl_space_type = "NLA_EDITOR"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return bool(len(context.scene.timeline_markers))

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        trigger = scene.timeline_trigger

        row = layout.row()
        row.label('Timeline Markers')

        #   list Timeline Markers
        row = layout.row()
        row.template_list("UI_UL_list", "timeline_markers", scene, "timeline_markers", trigger, "m_sel_marker", rows=2, maxrows=8)
        marker = context.scene.timeline_markers[trigger.m_sel_marker]

        if marker.name in context.scene.timeline_trigger.m_markerdict:
            #   assign Trigger to selected Timeline Marker
            row = layout.row()
            row.label('assign Trigger to Timeline Marker')
            row = layout.row(align=True)
            row.prop_search(trigger.m_markerdict[marker.name], "m_queue", trigger, "m_queues", text='', icon='VIEWZOOM')
            row.operator("blive.trigger_revoke", text="", icon="ZOOMOUT")

            box = layout.box()

            #   add items to trigger

            #   get selected Trigger Queue
            qid = trigger.m_markerdict[marker.name].m_queue
            queue = trigger.m_queues[qid]

            tbox = box.row(align=True)
            tbox.prop(queue, "m_pause", text="pause")
            tbox.prop(queue, "m_execute_after", text="send after")

            #    menu to choose new trigger
            tbox = box.row()
            tbox.operator_menu_enum("blive.trigger_append", "type", text="Add Trigger")

            #   list Trigger items
            for item in queue.m_slots:
                main = layout.column(align=True)
                head = main.box()
                split = head.split(percentage=0.75)
                row = split.row()
                if item.m_hidden:
                    row.prop(item, "m_hidden", text="", icon="TRIA_RIGHT", emboss=False)
                else:
                    row.prop(item, "m_hidden", text="", icon="TRIA_DOWN", emboss=False)
                row.label( item.m_type )
                split = split.split(percentage=1)
                buttons = split.column_flow(columns=1, align=True)
                buttons.operator("blive.trigger_remove", text="", icon="PANEL_CLOSE").m_slot = item.name

                if not item.m_hidden:
                    body = main.box()
                    triggertype = getattr(queue.m_trigger, item.m_type)
                    if hasattr(self, item.m_type):
                        getattr(self, item.m_type)(context, triggertype[item.name], body)
                    else:
                        row = body.row()
                        row.label("not implemented")

        #    we need to add a trigger first
        else:
            row = layout.row(align=True)
            row.operator("blive.trigger_new", text="Add Queue")

    def TriggerVideoOpen(self, context, trigger, ui):
        row = ui.row()
        row.prop(trigger, "m_filepath", text="Open File", icon="FILE_MOVIE")
        row = ui.row()
        row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
        row = ui.row()
        row.prop_search(trigger, "m_image", bpy.data, "images", text="image")
        row = ui.row()
        row.prop(trigger, "m_audio", text="audio")
        row = ui.row()
        row.prop(trigger, "m_loop", text="loop video")
        row = ui.row()
        row.prop(trigger, "m_preseek", text="preseek")
        row = ui.row()
        row.prop(trigger, "m_inp", text="inpoint")
        row.prop(trigger, "m_outp", text="outpoint")
        row = ui.row()
        row.prop(trigger, "m_deinterlace", text="deinterlace")


    def TriggerCameraOpen(self, context, trigger, ui):
        row = ui.row()
        row.prop(trigger, "m_filepath", text="Open File", icon="FILE_MOVIE")
        row = ui.row()
        row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
        row = ui.row()
        row.prop_search(trigger, "m_image", bpy.data, "images", text="image")
        row = ui.row(align=True)
        row.prop(trigger, "m_width", text="width")
        row.prop(trigger, "m_height", text="height")
        row = ui.row()
        row.prop(trigger, "m_deinterlace", text="deinterlace")

    def TriggerVideoState(self, context, trigger, ui):
        row = ui.row()
        row.prop(trigger, "m_state", text="")
        row = ui.row()
        row.prop_search(trigger, "m_image", bpy.data, "images", text="image")

    def TriggerDummy(self, context, trigger, ui):
        row = ui.row()
        row.prop(trigger, "m_msg", text="send Message")

    def TriggerChangeScene(self, context, trigger, ui):
        row = ui.row()
        row.prop_search(trigger, "m_scene", bpy.data, "scenes", text="scene")

    def TriggerGameProperty(self, context, trigger, ui):
        row = ui.row()
        row.prop_search(trigger, "m_object", context.scene, "objects", text="object")
        if not context.scene.objects[trigger.m_object].game.properties:
            return
        row = ui.row()
        row.prop_search(trigger, "m_property", context.scene.objects[trigger.m_object].game, "properties", text="prop")
        row = ui.row()
        row.prop(context.scene.objects[trigger.m_object].game.properties[trigger.m_property], "value", text="set")

def register():
    print("marker.ui.register")
    bpy.utils.register_class(BLive_PT_timeline_trigger)

def unregister():
    print("marker.ui.unregister")
    bpy.utils.unregister_class(BLive_PT_timeline_trigger)
