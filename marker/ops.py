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
from .props import TRIGGER_TYPE_ENUM
from ..utils.utils import unique_name

class BLive_OT_timeline_trigger_add_queue(bpy.types.Operator):
    '''add timeline marker trigger queue'''

    bl_idname = "blive.timeline_trigger_add_queue"
    bl_label = "BLive add timeline trigger queue"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        trigger = context.scene.timeline_marker_trigger
        queue = trigger.queues.add()
        trigger.active_queue = len(trigger.queues) -1
        queue.name = unique_name(trigger.queues, queue.name)

        return{'FINISHED'}

class BLive_OT_timeline_trigger_remove_queue(bpy.types.Operator):
    '''remove timeline marker trigger queue'''

    bl_idname = "blive.timeline_trigger_remove_queue"
    bl_label = "BLive remove timeline trigger queue"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        idx = context.scene.timeline_marker_trigger.active_queue
        return (idx > -1 and idx < len(context.scene.timeline_marker_trigger.queues))

    def execute(self, context):
        queues = context.scene.timeline_marker_trigger.queues
        idx = context.scene.timeline_marker_trigger.active_queue
        queues[idx].queue_slots.clear()
        queues.remove(idx)
        return{'FINISHED'}

class BLIVE_OT_timeline_trigger_add_slot(bpy.types.Operator):
    '''add timeline trigger queue slot'''

    bl_idname = "blive.timeline_trigger_add_slot"
    bl_label = "BLive add timeline trigger slot"
    bl_options = {'REGISTER', 'UNDO'}
    type = bpy.props.EnumProperty(name='type', default='TriggerScript', items=TRIGGER_TYPE_ENUM)

    @classmethod
    def poll(self, context):
        return context.scene.timeline_marker_trigger.queues

    def execute(self, context):
        trigger = bpy.context.scene.timeline_marker_trigger
        idx = trigger.active_queue
        queues = trigger.queues
        queue = queues[idx]

        slot = queue.queue_slots.add()
        slot.type = self.type

        data = getattr(trigger.data , slot.type).add()
        data.name = unique_name(getattr(trigger.data , slot.type), slot.type)

        slot.name = data.name

        return{'FINISHED'}

class BLive_OT_timeline_trigger_remove_slot(bpy.types.Operator):
    '''remove slot from timeline marker trigger'''

    bl_idname = "blive.timeline_trigger_remove_slot"
    bl_label = "BLive remove slot from timeline trigger"
    bl_options = {'REGISTER', 'UNDO'}
    slot = bpy.props.StringProperty()

    @classmethod
    def poll(self, context):
        trigger = bpy.context.scene.timeline_marker_trigger
        return len(trigger.queues[trigger.active_queue].queue_slots)

    def execute(self, context):
        trigger = bpy.context.scene.timeline_marker_trigger
        idx = trigger.active_queue
        queues = trigger.queues
        queue = queues[idx]

        keys = queue.queue_slots.keys()

        if not self.slot in keys:
            return{'CANCELLED'}

        slot = queue.queue_slots[self.slot]

        # remove data entry
        data = getattr(trigger.data , slot.type)
        data.remove(data.keys().index(slot.name))

        #remove queue_slot
        queue.queue_slots.remove( keys.index(self.slot) )

        return{'FINISHED'}

class BLive_OT_timeline_trigger_add_assign_marker(bpy.types.Operator):
    '''add timeline marker assign it to trigger queue'''

    bl_idname = "blive.timeline_trigger_add_assign_marker"
    bl_label = "BLive add and assign timeline marker to trigger"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        idx = context.scene.timeline_marker_trigger.active_queue
        queue = context.scene.timeline_marker_trigger.queues[idx]

        marker = context.scene.timeline_markers.new(name=queue.name, frame=context.scene.frame_current)
        queue.marker = marker.name
        return{'FINISHED'}

class BLive_OT_timeline_trigger_remove_revoke_marker(bpy.types.Operator):
    '''revoke timeline marker from trigger queue and remove it'''

    bl_idname = "blive.timeline_trigger_remove_revoke_marker"
    bl_label = "BLive revoke timeline marker from trigger and remove marker"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        idx = context.scene.timeline_marker_trigger.active_queue
        return len(context.scene.timeline_marker_trigger.queues[idx].marker)

    def execute(self, context):
        idx = context.scene.timeline_marker_trigger.active_queue
        queue = context.scene.timeline_marker_trigger.queues[idx]

        context.scene.timeline_markers.remove(context.scene.timeline_markers[queue.marker])
        queue.marker = ''

        return{'FINISHED'}

def register():
    print("marker.ops.register")
    bpy.utils.register_class(BLive_OT_timeline_trigger_add_queue)
    bpy.utils.register_class(BLive_OT_timeline_trigger_remove_queue)
    bpy.utils.register_class(BLIVE_OT_timeline_trigger_add_slot)
    bpy.utils.register_class(BLive_OT_timeline_trigger_remove_slot)
    bpy.utils.register_class(BLive_OT_timeline_trigger_add_assign_marker)
    bpy.utils.register_class(BLive_OT_timeline_trigger_remove_revoke_marker)

def unregister():
    print("marker.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_add_queue)
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_remove_queue)
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_add_slot)
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_remove_slot)
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_add_assign_marker)
    bpy.utils.unregister_class(BLive_OT_timeline_trigger_remove_revoke_marker)
