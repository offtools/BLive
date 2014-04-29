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

# TODO: use operators instead calling BLiveClient
#       TriggerScript, use import (module/function) instead of reading script everytime
#       reenable videotexture controls
#       remove dummy

import bpy
from liblo import Message
from ..common.libloclient import Client
from liblo import Message
from ..utils.utils import unique_name

TRIGGER_TYPE_ENUM = [
                    ("TriggerOpenVideo","Open Video","Open a Video"), \
                    ("TriggerOpenCamera","Connect Camera","Connect a Camera"), \
                    ("TriggerVideotextureState","Set Video State","Set Play, Pause, Stop"), \
                    ("TriggerChangeScene","Change active Scene","Change active Scene"), \
                    ("TriggerGameProperty","Set a Game Property","Set a Game Property"), \
                    ("TriggerScript","Run a Script","Run a script local"), \
                    ("TriggerOSCMessage","Send OSC Message","Send OSC Message") \
                    ]

class TriggerOpenVideo(bpy.types.PropertyGroup):
    object = bpy.props.StringProperty()

    def get_filepath(self):
        if not '_filepath' in self:
            self['_filepath'] = ''
        return self['_filepath']

    def set_filepath(self, f):
        self['_filepath'] = bpy.path.abspath(f)

    filepath = bpy.props.StringProperty(subtype="FILE_PATH", get=get_filepath, set=set_filepath)

    image = bpy.props.StringProperty()
    audio = bpy.props.BoolProperty()
    volume = bpy.props.FloatProperty(default=1.0, min=0.0, max=1.0)
    loop = bpy.props.BoolProperty(default=False)
    preseek = bpy.props.IntProperty(default=0)
    inp = bpy.props.FloatProperty(default=0.0)
    outp = bpy.props.FloatProperty(default=0.0)
    deinterlace = bpy.props.BoolProperty(default=False)

    def execute(self):
        m = Message("/bge/logic/media/openMovie",
                    self.object,
                    self.image,
                    self.filepath,
                    int(self.audio),
                    self.inp,
                    self.outp,
                    int(self.loop),
                    self.preseek,
                    int(self.deinterlace)
                    )

        Client().send(m)

class TriggerOpenCamera(bpy.types.PropertyGroup):
    object = bpy.props.StringProperty()
    device = bpy.props.StringProperty(default="/dev/video0")
    image = bpy.props.StringProperty()
    width = bpy.props.IntProperty(default=640, min=0)
    height = bpy.props.IntProperty(default=480, min=0)
    deinterlace = bpy.props.BoolProperty(default=False)
    rate = bpy.props.FloatProperty(default=0.0)

    def execute(self):
        m = Message("/bge/logic/media/openCamera",
                            self.object,
                            self.image,
                            self.filepath,
                            self.width,
                            self.height,
                            self.deinterlace,
                            self.rate
                            )
        Client().send(m)

class TriggerVideotextureState(bpy.types.PropertyGroup):
    image = bpy.props.StringProperty()
    state = bpy.props.EnumProperty(
    items = [("PLAY","play","play Video"),
            ("PAUSE","pause","pause Video"),
            ("STOP","stop","stop Video"),
            ("CLOSE","close","reset Texture")],
            name = "state")

    def execute(self):
        if self.state == "PLAY":
            Client().send(Message("/bge/logic/media/play", self.image))
        elif self.state == "PAUSE":
            Client().send(Message("/bge/logic/media/pause", self.image))
        elif self.state == "STOP":
            Client().send(Message("/bge/logic/media/stop", self.image))
        elif self.state == "CLOSE":
            Client().send(Message("/bge/logic/media/close", self.image))
        pass

class TriggerChangeScene(bpy.types.PropertyGroup):
    scene = bpy.props.StringProperty()

    def execute(self):
        #   change scene in blender too
        if self.scene in bpy.data.scenes:
            bpy.context.screen.scene = bpy.data.scenes[self.scene]
            Client().send(Message("/bge/scene/replace", self.scene))

class TriggerGameProperty(bpy.types.PropertyGroup):
    object = bpy.props.StringProperty()
    gameproperty = bpy.props.StringProperty()

    def execute(self):
        value = bpy.context.scene.objects[self.object].game.properties[self.gameproperty].value
        Client().send("/bge/scene/objects/gameproperty", self.object, self.gameproperty, value)

# TODO: use import (from string), add update routine
class TriggerScript(bpy.types.PropertyGroup):
    script = bpy.props.StringProperty()

    def execute(self):
        if self.script in bpy.data.texts:
            exec(bpy.data.texts[self.script].as_string())

class TriggerOSCMessage(bpy.types.PropertyGroup):
    msg = bpy.props.StringProperty()

    def execute(self):
        # test if first arg contains '/' (path)
        if self.msg.split(' ')[0].count('/'):
            msg = Message(self.msg.split(' ')[0])
            for i in self.msg.split(' ')[1:]:
                # digits are ints
                if i.isdigit():
                    msg.add(int(i))
                # try convert args with '.' to float otherwise stays string
                elif i.count('.') == 1:
                    try:
                        msg.add(float(i))
                    except ValueError:
                        msg.add(i)
                # all other args parsed as strings
                else:
                    msg.add(i)
            Client().send(msg)

class TimelineMarkerDictItem(bpy.types.PropertyGroup):
    '''single Item of a TimelineMarker Trigger Dictionary'''

    # queue - refences a Trigger Queue
    def get_queue(self):
        # return a queue
        pass

    queue = bpy.props.StringProperty() #get=get_queue)

class TimelineMarkerQueueData(bpy.types.PropertyGroup):
    '''TimelineMarkerQueueData holds all Triggers'''
    TriggerOpenVideo = bpy.props.CollectionProperty(type=TriggerOpenVideo)
    TriggerOpenCamera = bpy.props.CollectionProperty(type=TriggerOpenCamera)
    TriggerVideotextureState = bpy.props.CollectionProperty(type=TriggerVideotextureState)
    TriggerChangeScene = bpy.props.CollectionProperty(type=TriggerChangeScene)
    TriggerGameProperty = bpy.props.CollectionProperty(type=TriggerGameProperty)
    TriggerScript = bpy.props.CollectionProperty(type=TriggerScript)
    TriggerOSCMessage = bpy.props.CollectionProperty(type=TriggerOSCMessage)

class TimelineMarkerQueueSlot(bpy.types.PropertyGroup):
    '''TimelineMarker QueueSlots referencing Triggers by name and type'''

    # Slot Trigger Type
    type = bpy.props.EnumProperty(default='TriggerOpenVideo', items=TRIGGER_TYPE_ENUM)

    # references a Trigger
    def get_data(self):
        # returns trigger from TimelineMarkerTrigger.data
        pass

    def set_data(self, value):
        # update users property of the Trigger
        pass

    # references Trigger Data
    #data = bpy.props.StringProperty()

    # show data in ui
    show_all = bpy.props.BoolProperty(default=False)

class TimelineMarkerQueue(bpy.types.PropertyGroup):
    '''Trigger Queue, which refences multiple Triggers'''

    def set_marker(self, value):
        tr = bpy.context.scene.timeline_marker_trigger

        # clear old marker dict entries
        if '_marker' in self:
            if value in tr.marker_dict:
                queue = tr.queues[tr.marker_dict[value].queue]
                queue.marker = ''
            if self['_marker'] in tr.marker_dict:
                idx = tr.marker_dict.keys().index(self['_marker'])
                tr.marker_dict.remove(idx)

        self['_marker'] = value

        # empty value means revoke marker
        if not len(value):
            return

        if not self['_marker'] in tr.marker_dict:
            item = tr.marker_dict.add()
            item.name = self['_marker']
        tr.marker_dict[self['_marker']].queue = self.name

    def get_marker(self):
        if not '_marker' in self:
            self['_marker'] = ''
        return self['_marker']

    marker = bpy.props.StringProperty(default='', get=get_marker, set=set_marker)

    # overwrite behaviour of name property, to ensure unique names
    def update_name(self, context):
        # set unique trigger name
        if context.scene.timeline_marker_trigger.queues.keys().count(self.name) > 1:
            self.name = unique_name(context.scene.timeline_marker_trigger.queues, self.name)
        # write new name into marker dictionary
        self.marker = self.marker

    name = bpy.props.StringProperty(default='Trigger',update=update_name)

    # collection of queue slots, holds name and type of the queue_items
    queue_slots = bpy.props.CollectionProperty(type=TimelineMarkerQueueSlot)

    # active / selected slot
    # TODO: check for outside removed triggers and cleanup
    def update_active(self, context):
        pass

    active_queue_slot = bpy.props.IntProperty(default=-1)

    # trigger behaviour
    execute_after = bpy.props.BoolProperty(default=False)
    pause = bpy.props.BoolProperty(default=True)

class TimelineMarkerTrigger(bpy.types.PropertyGroup):
    '''Triggers for TimelineMarkers'''

    # acts as dictionary to find trigger by marker names (used by handler)
    marker_dict = bpy.props.CollectionProperty(type=TimelineMarkerDictItem)

    # trigger queue, which holds a collection of trigger which can be assigned to a marker position
    queues = bpy.props.CollectionProperty(type=TimelineMarkerQueue)

    # collection of all triggers
    data = bpy.props.PointerProperty(name='data', type=TimelineMarkerQueueData)

    # active queue in the ui
    active_queue = bpy.props.IntProperty(default=-1)

def register():
    print("marker.props.register")

    bpy.utils.register_class(TriggerScript)
    bpy.utils.register_class(TriggerOSCMessage)
    bpy.utils.register_class(TriggerOpenVideo)
    bpy.utils.register_class(TriggerOpenCamera)
    bpy.utils.register_class(TriggerVideotextureState)
    bpy.utils.register_class(TriggerChangeScene)
    bpy.utils.register_class(TriggerGameProperty)

    bpy.utils.register_class(TimelineMarkerQueueData)
    bpy.utils.register_class(TimelineMarkerQueueSlot)
    bpy.utils.register_class(TimelineMarkerQueue)
    bpy.utils.register_class(TimelineMarkerDictItem)
    bpy.utils.register_class(TimelineMarkerTrigger)

    bpy.types.Scene.timeline_marker_trigger = bpy.props.PointerProperty(type=TimelineMarkerTrigger, options={"HIDDEN"})

def unregister():
    print("marker.props.unregister")

    del bpy.types.Scene.timeline_marker_trigger

    bpy.utils.unregister_class(TriggerScript)
    bpy.utils.unregister_class(TriggerOSCMessage)
    bpy.utils.unregister_class(TriggerOpenVideo)
    bpy.utils.unregister_class(TriggerOpenCamera)
    bpy.utils.unregister_class(TriggerVideotextureState)
    bpy.utils.unregister_class(TriggerChangeScene)
    bpy.utils.unregister_class(TriggerGameProperty)

    bpy.utils.unregister_class(TimelineMarkerTrigger)
    bpy.utils.unregister_class(TimelineMarkerDictItem)
    bpy.utils.unregister_class(TimelineMarkerQueue)
    bpy.utils.unregister_class(TimelineMarkerQueueSlot)
    bpy.utils.unregister_class(TimelineMarkerQueueData)
