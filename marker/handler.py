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
from . import props
from bpy.app.handlers import persistent
from ..common.libloclient import Client

@persistent
def marker_handler(scene):
    '''app handler mainly used to trigger timelinemarkers
    '''
    # ignored if animation is not playing
    if not bpy.context.screen.is_animation_playing:
        return

    current_frame = scene.frame_current
    prev_frame = current_frame - 1

    trigger = scene.timeline_marker_trigger

    marked_frames = dict()
    for i in trigger.marker_dict:
        if i.name in scene.timeline_markers:
            marked_frames[scene.timeline_markers[i.name].frame] = i

    def execute_slot(frame, is_current):
        if frame in marked_frames:
            marker = trigger.marker_dict[marked_frames[frame].name]
            queue = trigger.queues[marker.queue]

            if is_current and queue.pause and bpy.context.screen.is_animation_playing:
                bpy.ops.screen.animation_play()

            if (not queue.execute_after and is_current) or (queue.execute_after and not is_current):
                for slot in queue.queue_slots:
                    slot_data = getattr(trigger.data, slot.type)[slot.name]
                    slot_data.execute()

    execute_slot(frame=current_frame, is_current=True)
    execute_slot(frame=prev_frame, is_current=False)

def register():
    print("marker.handler.register")
    Client().add_apphandler('frame_change_pre', marker_handler)

def unregister():
    print("marker.handler.unregister")

