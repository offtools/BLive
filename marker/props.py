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

# TODO: user operators instead calling BLiveClient

import bpy
from liblo import Message
from ..common.libloclient import Client
from liblo import Message

TRIGGER_TYPE_ENUM = [("TriggerDummy","Dummy","Dummy Trigger"), \
                    ("TriggerVideoOpen","Open Video","Open a Video"), \
                    ("TriggerCameraOpen","Connect Camera","Connect a Camera"), \
                    ("TriggerVideoState","Set Video State","Set Play, Pause, Stop"), \
                    ("TriggerChangeScene","Change active Scene","Change active Scene"), \
                    ("TriggerGameProperty","Set a Game Property","Set a Game Property"), \
                    ("TriggerScript","Run a Script","Run a script local"), \
                    ("TriggerOSCMessage","Send OSC Message","Send OSC Message") \
                    ]

def TRIGGER_TYPE_NAME(self, _type):
    types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
    return TRIGGER_TYPE_ENUM[types.index(_type)][1]

def TRIGGER_TYPE_DESCRIPTION(_type):
    types = [ i[0] for i in TRIGGER_TYPE_ENUM ]
    return TRIGGER_TYPE_ENUM[types.index(_type)][2]

class TriggerDummy(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    m_oscpath = bpy.props.StringProperty(default="/debug")

    m_msg = bpy.props.StringProperty(default="Dummy Trigger")

    def send(self):
        Client().send(self.m_oscpath, self.m_msg)

class TriggerVideoOpen(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    m_oscpath = bpy.props.StringProperty(default="/texture/movie/open")

    m_object = bpy.props.StringProperty()
    m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    m_image = bpy.props.StringProperty()
    m_audio = bpy.props.BoolProperty()
    m_loop = bpy.props.BoolProperty(default=False)
    m_preseek = bpy.props.IntProperty(default=0)
    m_inp = bpy.props.FloatProperty(default=0.0)
    m_outp = bpy.props.FloatProperty(default=0.0)
    m_deinterlace = bpy.props.BoolProperty(default=False)

    def send(self):
        filepath = bpy.path.abspath(self.m_filepath)
        m = Message("/bge/logic/media/openMovie",
                    self.m_object,
                    self.m_image,
                    filepath,
                    int(self.m_audio),
                    self.m_inp,
                    self.m_outp,
                    int(self.m_loop),
                    self.m_preseek,
                    int(self.m_deinterlace)
                    )

        Client().send(m)

class TriggerCameraOpen(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    m_oscpath = bpy.props.StringProperty(default="/texture/camera")

    m_object = bpy.props.StringProperty()
    m_filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    m_image = bpy.props.StringProperty()

    m_width = bpy.props.IntProperty(default=640, min=0)
    m_height = bpy.props.IntProperty(default=480, min=0)
    m_deinterlace = bpy.props.BoolProperty(default=False)
    m_rate = bpy.props.FloatProperty(default=0.0)

    def send(self):
        m = Message("/bge/logic/media/openCamera",
                            self.m_object,
                            self.m_image,
                            self.m_filepath,
                            self.m_width,
                            self.m_height,
                            self.m_deinterlace,
                            self.m_rate
                            )
        Client().send(m)

class TriggerVideoState(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    #~ m_oscpath = bpy.props.StringProperty(default="/texture/state")

    m_image = bpy.props.StringProperty()
    m_state = bpy.props.EnumProperty(
    items = [("PLAY","play","play Video"),
            ("PAUSE","pause","pause Video"),
            ("STOP","stop","stop Video"),
            ("CLOSE","close","reset Texture")],
            name = "state")

    def send(self):
        if self.m_state == "PLAY":
            Client().send(Message("/bge/logic/media/play", self.m_image))
        elif self.m_state == "PAUSE":
            Client().send(Message("/bge/logic/media/pause", self.m_image))
        elif self.m_state == "STOP":
            Client().send(Message("/bge/logic/media/stop", self.m_image))
        elif self.m_state == "CLOSE":
            Client().send(Message("/bge/logic/media/close", self.m_image))
        pass

class TriggerChangeScene(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    m_oscpath = bpy.props.StringProperty(default="/bge/scene/replace")
    m_scene = bpy.props.StringProperty()

    def send(self):
        #   change scene in blender too
        bpy.context.screen.scene = bpy.data.scenes[self.m_scene]
        Client().send(Message(self.m_oscpath, self.m_scene))

class TriggerGameProperty(bpy.types.PropertyGroup):
    m_hidden = bpy.props.BoolProperty(default=True)
    m_oscpath = bpy.props.StringProperty(default="/bge/scene/objects/gameproperty")

    m_object = bpy.props.StringProperty()
    m_property = bpy.props.StringProperty()

    def send(self):
        value = bpy.context.scene.objects[self.m_object].game.properties[self.m_property].value
        Client().send(self.m_oscpath, self.m_object, self.m_property, value)

class TriggerScript(bpy.types.PropertyGroup):
    m_script = bpy.props.StringProperty()

    def send(self):
        if self.m_script in bpy.data.texts:
            exec(bpy.data.texts[self.m_script].as_string())

class TriggerOSCMessage(bpy.types.PropertyGroup):
    m_msg = bpy.props.StringProperty()

    def send(self):
        # test if first arg contains '/' (path)
        if self.m_msg.split(' ')[0].count('/'):
            msg = Message(self.m_msg.split(' ')[0])
            for i in self.m_msg.split(' ')[1:]:
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

class TriggerWrapper(bpy.types.PropertyGroup):
    '''
        Property Group for OscTrigger
    '''
    TriggerDummy = bpy.props.CollectionProperty(type=TriggerDummy)
    TriggerVideoOpen = bpy.props.CollectionProperty(type=TriggerVideoOpen)
    TriggerCameraOpen = bpy.props.CollectionProperty(type=TriggerCameraOpen)
    TriggerVideoState = bpy.props.CollectionProperty(type=TriggerVideoState)
    TriggerChangeScene = bpy.props.CollectionProperty(type=TriggerChangeScene)
    TriggerGameProperty = bpy.props.CollectionProperty(type=TriggerGameProperty)
    TriggerScript = bpy.props.CollectionProperty(type=TriggerScript)
    TriggerOSCMessage = bpy.props.CollectionProperty(type=TriggerOSCMessage)

class TriggerSlot(bpy.types.PropertyGroup):
    m_type = bpy.props.StringProperty()
    m_hidden = bpy.props.BoolProperty(default=True)

class TriggerQueue(bpy.types.PropertyGroup):
    m_execute_after = bpy.props.BoolProperty(default=False)
    m_pause = bpy.props.BoolProperty(default=True)
    m_trigger = bpy.props.PointerProperty(type=TriggerWrapper)
    m_slots = bpy.props.CollectionProperty(type=TriggerSlot)
    m_sel_slot = bpy.props.StringProperty()

class MarkerDict(bpy.types.PropertyGroup):
    m_queue = bpy.props.StringProperty()

class TimelineTrigger(bpy.types.PropertyGroup):
    m_markerdict = bpy.props.CollectionProperty(type=MarkerDict)
    m_queues = bpy.props.CollectionProperty(type=TriggerQueue)
    m_sel_marker = bpy.props.IntProperty(default = 0)

def register():
    print("marker.props.register")

    bpy.utils.register_class(TriggerScript)
    bpy.utils.register_class(TriggerOSCMessage)
    bpy.utils.register_class(TriggerDummy)
    bpy.utils.register_class(TriggerVideoOpen)
    bpy.utils.register_class(TriggerCameraOpen)
    bpy.utils.register_class(TriggerVideoState)
    bpy.utils.register_class(TriggerChangeScene)
    bpy.utils.register_class(TriggerGameProperty)
    bpy.utils.register_class(TriggerWrapper)
    bpy.utils.register_class(TriggerSlot)
    bpy.utils.register_class(TriggerQueue)
    bpy.utils.register_class(MarkerDict)
    bpy.utils.register_class(TimelineTrigger)

    bpy.types.Scene.timeline_trigger = bpy.props.PointerProperty(type=TimelineTrigger, options={"HIDDEN"})

def unregister():
    print("marker.props.unregister")

    del bpy.types.Scene.timeline_trigger

    bpy.utils.unregister_class(TriggerScript)
    bpy.utils.unregister_class(TriggerOSCMessage)
    bpy.utils.unregister_class(TriggerDummy)
    bpy.utils.unregister_class(TriggerVideoOpen)
    bpy.utils.unregister_class(TriggerCameraOpen)
    bpy.utils.unregister_class(TriggerVideoState)
    bpy.utils.unregister_class(TriggerChangeScene)
    bpy.utils.unregister_class(TriggerGameProperty)
    bpy.utils.unregister_class(TriggerQueue)
    bpy.utils.unregister_class(TriggerSlot)
    bpy.utils.unregister_class(TriggerWrapper)
    bpy.utils.unregister_class(MarkerDict)
    bpy.utils.unregister_class(TimelineTrigger)
