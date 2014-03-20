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
from ..common.libloclient import Client

#type_enum = (('actions', 'Action', 'Action', 'ACTION', 0),
        #('armatures', 'Armature', 'Armature', 'ARMATURE_DATA', 1),
        #('brushes', 'brushes', 'brushes', 'BRUSH_DATA', 2),
        #('cameras', 'Cameras', 'Cameras', 'CAMERA_DATA', 3),
        #('curves', 'curves', 'curves'),
        #('filepath', 'filepath', 'filepath'),
        #('fonts', 'fonts', 'fonts'),
        #('grease_pencil', 'grease_pencil', 'grease_pencil'),
        #('groups', 'groups', 'groups'),
        #('images', 'images', 'images'),
        #('lamps', 'lamps', 'lamps'),
        #('lattices', 'lattices', 'lattices'),
        #('libraries', 'libraries', 'libraries'),
        #('linestyles', 'linestyles', 'linestyles'),
        #('masks', 'masks', 'masks'),
        #('materials', 'materials', 'materials'),
        #('meshes', 'meshes', 'meshes'),
        #('metaballs', 'metaballs', 'metaballs'),
        #('movieclips', 'movieclips', 'movieclips'),
        #('node_groups', 'node_groups', 'node_groups'),
        #('objects', 'Objects', 'Objects', 'OBJECT_DATA'),
        #('particles', 'particles', 'particles'),
        #('scenes', 'scenes', 'scenes'),
        #('screens', 'screens', 'screens'),
        #('scripts', 'scripts', 'scripts'),
        #('shape_keys', 'shape_keys', 'shape_keys'),
        #('sounds', 'sounds', 'sounds'),
        #('speakers', 'speakers', 'speakers'),
        #('texts', 'texts', 'texts'),
        #('textures', 'textures', 'textures'),
        #('window_managers', 'window_managers', 'window_managers'),
        #('worlds', 'worlds', 'worlds')
        #)

type_enum = (('actions', 'Action', 'Action'),
        ('armatures', 'Armature', 'Armature'),
        ('brushes', 'brushes', 'brushes'),
        ('cameras', 'cameras', 'cameras'),
        ('curves', 'curves', 'curves'),
        ('filepath', 'filepath', 'filepath'),
        ('fonts', 'fonts', 'fonts'),
        ('grease_pencil', 'grease_pencil', 'grease_pencil'),
        ('groups', 'groups', 'groups'),
        ('images', 'images', 'images'),
        ('lamps', 'lamps', 'lamps'),
        ('lattices', 'lattices', 'lattices'),
        ('libraries', 'libraries', 'libraries'),
        ('linestyles', 'linestyles', 'linestyles'),
        ('masks', 'masks', 'masks'),
        ('materials', 'materials', 'materials'),
        ('meshes', 'meshes', 'meshes'),
        ('metaballs', 'metaballs', 'metaballs'),
        ('movieclips', 'movieclips', 'movieclips'),
        ('node_groups', 'node_groups', 'node_groups'),
        ('objects', 'Objects', 'Objects'),
        ('particles', 'particles', 'particles'),
        ('scenes', 'scenes', 'scenes'),
        ('screens', 'screens', 'screens'),
        ('scripts', 'scripts', 'scripts'),
        ('shape_keys', 'shape_keys', 'shape_keys'),
        ('sounds', 'sounds', 'sounds'),
        ('speakers', 'speakers', 'speakers'),
        ('texts', 'texts', 'texts'),
        ('textures', 'textures', 'textures'),
        ('window_managers', 'window_managers', 'window_managers'),
        ('worlds', 'worlds', 'worlds')
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

    def execute(self, arg):
        if self.module in globals():
            m = globals()[self.module]
            getattr(m, self.function)(arg)
        else:
            m = __import__(self.module)
            getattr(m, self.function)(arg)

class OscDmxPropertyHandler(OscDmxHandler):
    """oscdmx maps to channels to id data properties"""
    type_enum = bpy.props.StringProperty()
    id_data = bpy.props.StringProperty()
    data_path = bpy.props.StringProperty()
    index = bpy.props.IntProperty(default=-1)
    min = bpy.props.FloatProperty()
    max = bpy.props.FloatProperty()

    def execute(self, arg):
        ob = getattr(bpy.data, self.type_enum)[self.id_data]
        if hasattr(getattr(ob, self.data_path), '__len__'):
            getattr(ob, self.data_path)[self.index] = arg
        else:
            setattr(ob, self.data_path, arg)

class OscDmxChannel(bpy.types.PropertyGroup):
    """oscdmx channel"""
    registered = bpy.props.BoolProperty(default=False)
    properties = bpy.props.CollectionProperty(type=OscDmxPropertyHandler)
    script = bpy.props.CollectionProperty(type=OscDmxScriptHandler)
    idx1 = bpy.props.IntProperty(default=0, subtype='UNSIGNED')
    idx2 = bpy.props.IntProperty(default=-1, subtype='UNSIGNED')

    def __iter__(self):
        return self

    def __next__(self):
        l = [self.properties, self.script]

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
    sel_type = bpy.props.EnumProperty(name='ID Type', items=type_enum)
    sel_item = bpy.props.StringProperty()
    sel_dpath = bpy.props.StringProperty()
    sel_chan = bpy.props.IntProperty(default=0, min=0, max=254)
    sel_method = bpy.props.EnumProperty(name='Method', items=method_enum)
    sel_module = bpy.props.StringProperty()
    sel_function = bpy.props.StringProperty()
    channels = bpy.props.CollectionProperty(type=OscDmxChannel)

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
    bpy.utils.register_class(OscDmxScriptHandler)
    bpy.utils.register_class(OscDmxHandler)
    bpy.utils.unregister_class(OscDmxChannel)
    bpy.utils.unregister_class(OscDmx)
