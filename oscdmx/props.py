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
import sys
import re
from ..common.libloclient import Client

type_enum = (('actions', 'Action', 'Action', 'ACTION', 0),
        ('armatures', 'Armature', 'Armature', 'ARMATURE_DATA', 1),
        ('brushes', 'Brushes', 'Brushes', 'BRUSH_DATA', 2),
        ('cameras', 'Cameras', 'Cameras', 'CAMERA_DATA', 3),
        ('curves', 'Curves', 'Curves', 'CURVE_DATA', 4),
        ('filepath', 'Filepath', 'Filepath', 'FILE', 5),
        ('fonts', 'Fonts', 'Fonts', 'FONT_DATA', 6),
        ('grease_pencil', 'Grease Pencil', 'Grease Pencil', 'GREASEPENCIL', 7),
        ('groups', 'Groups', 'Groups', 'GROUP', 8),
        ('images', 'Images', 'Images', 'IMAGE_DATA', 9),
        ('lamps', 'Lamps', 'Lamps', 'LAMP_DATA', 10),
        ('lattices', 'Lattices', 'Lattices', 'LATTICE_DATA', 11),
        ('libraries', 'Libraries', 'Libraries', 'LIBRARY_DATA_DIRECT', 12),
        ('linestyles', 'Linestyles', 'Linestyles', 'LINE_DATA', 13),
        ('masks', 'Masks', 'Masks', 'MOD_MASK', 14),
        ('materials', 'Materials', 'Materials', 'MATERIAL_DATA', 15),
        ('meshes', 'Meshes', 'Meshes', 'MESH_DATA', 16),
        ('metaballs', 'Metaballs', 'Metaballs', 'META_BALL', 17),
        ('movieclips', 'Movieclips', 'Movieclips', 'FILE_MOVIE', 18),
        ('node_groups', 'Node_groups', 'Node_groups', 'NODE', 19),
        ('objects', 'Objects', 'Objects', 'OBJECT_DATA', 20),
        ('particles', 'Particles', 'Particles', 'PARTICLE_DATA', 21),
        ('scenes', 'Scenes', 'Scenes', 'SCENE_DATA', 22),
        ('screens', 'Screens', 'Screens', '‘SPLITSCREEN', 23),
        ('scripts', 'Scripts', 'Scripts', 'SCRIPT', 24),
        ('shape_keys', 'Shape_keys', 'Shape_keys', 'SHAPEKEY_DATA', 25),
        ('sounds', 'Sounds', 'Sounds', 'SOUND', 26),
        ('speakers', 'Speakers', 'Speakers', 'SPEAKER', 27),
        ('texts', 'Texts', 'Texts', 'TEXT', 28),
        ('textures', 'Textures', 'Textures', 'TEXTURE_DATA', 29),
        ('window_managers', 'Window_managers', 'Window_managers', 'FULLSCREEN', 30),
        ('worlds', 'Worlds', 'Worlds', 'WORLD_DATA', 31)
        )

method_enum = (('properties', 'Properties', 'Properties'),
        ('script', 'Script', 'Script'))

class OscDmxHandler(bpy.types.PropertyGroup):
    def execute(self, arg):
        pass

class OscDmxScriptHandler(OscDmxHandler):
    """oscdmx maps to channels to custom scripts"""
    module = bpy.props.StringProperty()
    function = bpy.props.StringProperty()

    def execute(self, chan, arg):
        if self.module in sys.modules:
            m = sys.modules[self.module[:-3]]
            getattr(m, self.function)()
        else:
            m = __import__(self.module[:-3])
            getattr(m, self.function)(chan, arg)

def check_array(self, context):
    if hasattr(self.data_path, '__len__') and '[' in self.data_path:
        pattern=re.compile(r"[\[\]]")
        sp = pattern.split(self.data_path)
        self.data_path = sp[0]
        self.index = int(sp[1])
    else:
        self.index = -1

class OscDmxPropertyHandler(OscDmxHandler):
    """oscdmx maps to channels to id data properties"""
    type_enum = bpy.props.EnumProperty(name='ID Type', items=type_enum)
    id_data = bpy.props.StringProperty()
    data_path = bpy.props.StringProperty(update=check_array)
    index = bpy.props.IntProperty(default=-1)
    min = bpy.props.FloatProperty(default=0.0)
    max = bpy.props.FloatProperty(default=1.0)

    def execute(self, chan, arg):
        ob = getattr(bpy.data, self.type_enum)[self.id_data]
        conv = ((self.max-self.min)*arg)+self.min
        if hasattr(getattr(ob, self.data_path), '__len__'):
            getattr(ob, self.data_path)[self.index] = conv
        else:
            setattr(ob, self.data_path, conv)

class OscDmxChannel(bpy.types.PropertyGroup):
    """oscdmx channel"""
    registered = bpy.props.BoolProperty(default=False)
    properties = bpy.props.CollectionProperty(type=OscDmxPropertyHandler)
    scripts = bpy.props.CollectionProperty(type=OscDmxScriptHandler)
    idx1 = bpy.props.IntProperty(default=0, subtype='UNSIGNED')
    idx2 = bpy.props.IntProperty(default=-1, subtype='UNSIGNED')

    def add_handler(self, method):
        pass

    def remove_handler(self, handler):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        l = [self.properties, self.scripts]

        if self.idx2 < (len(l[self.idx1])-1) and len(l[self.idx1]) > 0:
            self.idx2  = self.idx2 + 1
        else:
            self.idx2 = 0
            if self.idx1 < (len(l) - 1):
                self.idx1 = self.idx1 + 1
                if not len(l[self.idx1]):
                    while not len(l[self.idx1]) and self.idx1 < (len(l) - 1):
                        print("+1")
                        self.idx1 = self.idx1 + 1
                    if not self.idx1 < len(l) or not len(l[self.idx1]):
                        self.idx1 = 0
                        self.idx2 = -1
                        raise StopIteration
            else:
                self.idx1 = 0
                self.idx2 = -1
                raise StopIteration
        return l[self.idx1][self.idx2]

class OscDmx(bpy.types.PropertyGroup):
    """oscdmx"""
    path_prefix = bpy.props.StringProperty(name="Prefix", default="/0/dmx")
    channels = bpy.props.CollectionProperty(type=OscDmxChannel)
    active_channel =  bpy.props.IntProperty(default=0, min=0, max=254)
    active_channel_by_name =  bpy.props.IntProperty(default=0, min=0, max=254)
    active_script_handler =  bpy.props.IntProperty(default=0, subtype='UNSIGNED')
    active_prop_handler =  bpy.props.IntProperty(default=0, subtype='UNSIGNED')
    sel_method = bpy.props.EnumProperty(name='Method', items=method_enum)


def register():
    print("oscdmx.props.register")
    bpy.utils.register_class(OscDmxHandler)
    bpy.utils.register_class(OscDmxScriptHandler)
    bpy.utils.register_class(OscDmxPropertyHandler)
    bpy.utils.register_class(OscDmxChannel)
    bpy.utils.register_class(OscDmx)

    bpy.types.Scene.oscdmx = bpy.props.PointerProperty(type=OscDmx)

def unregister():
    print("oscdmx.props.unregister")
    bpy.utils.unregister_class(OscDmxPropertyHandler)
    bpy.utils.unregister_class(OscDmxScriptHandler)
    bpy.utils.unregister_class(OscDmxHandler)
    bpy.utils.unregister_class(OscDmxChannel)
    bpy.utils.unregister_class(OscDmx)
