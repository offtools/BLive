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

# TODO: add basic blive_init on every startup (only path append and import statement)

import bpy
# TODO: remove import os, sys later
import os
import sys
import time
import subprocess
from liblo import Bundle, Message
from .libloclient import Client
from ..utils.utils import import_path

INITSCRIPT = "blive_init.py"
UPDATESCRIPT = "blive_update.py"

class BLive_OT_start_gameengine(bpy.types.Operator):
    bl_idname = "blive.gameengine_start"
    bl_label = "BLive start gameengine"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty()
    files = bpy.props.CollectionProperty(name="File Path",type=bpy.types.OperatorFileListElement)
    directory = bpy.props.StringProperty(subtype='DIR_PATH')

    def add_start_script(self):
        '''create startup script
        '''

        if not INITSCRIPT in bpy.data.texts:
            bpy.data.texts.new(name=INITSCRIPT)
        else:
            bpy.data.texts['Text'].clear()

        textblock = bpy.data.texts[INITSCRIPT]
        textblock.write("import sys\n")
        textblock.write("sys.path.append(r'{0}')\n".format(import_path()))
        textblock.write("import gameengine\n")
        textblock.write("port=%s\n"%(bpy.context.window_manager.blive_settings.port))
        textblock.write("gameengine.register(port)\n")

    def add_update_script(self):
        '''create update script
        '''

        if not UPDATESCRIPT in bpy.data.texts:
            bpy.data.texts.new(name=UPDATESCRIPT)

        textblock = bpy.data.texts[UPDATESCRIPT]
        textblock.write('import bge\n')
        textblock.write('try:\n')
        textblock.write('\tif hasattr(bge.logic, "server"):\n')
        textblock.write('\t\twhile bge.logic.server.recv(0): pass\n')
        textblock.write('except AttributeError:\n')
        textblock.write('\tpass\n')

    def add_logic(self, sc):
        '''create gamelogic bricks
        '''

        # active in scene camera holds game logic
        if not sc.camera:
            bpy.ops.object.camera_add()
            for ob in sc.objects:
                if ob.type == 'CAMERA':
                    sc.camera = ob #set object as camera
                    break

        sc.objects.active = sc.camera #make camera active

        if not 's.init' in sc.camera.game.sensors:
            bpy.ops.logic.sensor_add(type='ALWAYS', name='s.init')
        sc.camera.game.sensors['s.init'].use_pulse_true_level = False
        sc.camera.game.sensors['s.init'].use_pulse_false_level = False

        if not 's.update' in sc.camera.game.sensors:
            bpy.ops.logic.sensor_add(type='ALWAYS', name='s.update')
        sc.camera.game.sensors['s.update'].use_pulse_true_level = True
        sc.camera.game.sensors['s.update'].use_pulse_false_level = False
        sc.camera.game.sensors['s.update'].frequency = 0

        if not 'c.init' in sc.camera.game.controllers:
            bpy.ops.logic.controller_add(type='PYTHON', name='c.init')
        sc.camera.game.controllers['c.init'].mode = 'SCRIPT'
        sc.camera.game.controllers['c.init'].text = bpy.data.texts[INITSCRIPT]

        if not 'c.update' in sc.camera.game.controllers:
            bpy.ops.logic.controller_add(type='PYTHON', name='c.update')
        sc.camera.game.controllers['c.update'].mode = 'SCRIPT'
        sc.camera.game.controllers['c.update'].text = bpy.data.texts[UPDATESCRIPT]

        sc.camera.game.sensors['s.init'].link(sc.camera.game.controllers['c.init'])
        sc.camera.game.sensors['s.update'].link(sc.camera.game.controllers['c.update'])

    def fork(self, context):
        # fork blenderplayer
        sc = context.scene
        bc = context.window_manager.blive_settings
        server = bc.server
        port = bc.port

        app = "blenderplayer"
        blendfile = context.blend_data.filepath
        sep = '-'
        portarg = "-p {0}".format(port)
        cmd = [app,  blendfile, sep, portarg]
        blendprocess = subprocess.Popen(cmd)

        Client().connect(server, port)

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        # add scripts
        self.add_start_script()
        self.add_update_script()

        # add logic to every scene
        curscene = bpy.context.screen.scene #save current active scene

        for sc in bpy.data.scenes:
            # fix render resolution
            context.scene.render.resolution_x = context.scene.game_settings.resolution_x
            context.scene.render.resolution_y = context.scene.game_settings.resolution_y
            # change active scene and add logic
            context.screen.scene=sc
            self.add_logic(sc)

        context.screen.scene = curscene #restore scene

        # save snapshot into tmp
        #filepath = os.path.join(context.user_preferences.filepaths.temporary_directory, "blive-{0}".format(int(time.time())))
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath)

        self.fork(context)

        return{'FINISHED'}

    def invoke(self, context, event):
        if not context.blend_data.filepath:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.fork(context)
            return {'FINISHED'}

class BLive_OT_stop_gameengine(bpy.types.Operator):
    bl_idname = "blive.gameengine_stop"
    bl_label = "BLive stop gameengine"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        # send disconnect to quit gameengine
        Client().send(Message("/bge/logic/endGame"))
        return{'FINISHED'}


class BLive_OT_reload_gameengine(bpy.types.Operator):
    bl_idname = "blive.gameengine_reload"
    bl_label = "BLive reload gameengine"

    #@classmethod
    #def poll(self, context):
        #pass

    def execute(self, context):
        # reload gameengine by sending restartGame(), without closing
        Client().send(Message("/bge/logic/restartGame"))
        return{'FINISHED'}

class BLive_OT_save_reload_gameengine(bpy.types.Operator):
    bl_idname = "blive.gameengine_save_reload"
    bl_label = "BLive save and reload gameengine"

    @classmethod
    def poll(self, context):
        return bool(context.blend_data.filepath)

    def execute(self, context):
        # reload gameengine by sending restartGame(), without closing
        # get updates, if Objects are added or removed in a scene
        bpy.ops.wm.save_as_mainfile(filepath=bpy.context.blend_data.filepath)
        Client().send(Message("/bge/logic/restartGame"))
        return{'FINISHED'}

class BLive_OT_restart_gameengine(bpy.types.Operator):
    bl_idname = "blive.gameengine_restart"
    bl_label = "BLive restart gameengine"

    #@classmethod
    #def poll(self, context):
        #pass

    def execute(self, context):
        # stop gameengine
        bpy.ops.blive.gameengine_stop()
        # start gameengine
        bpy.ops.blive.gameengine_start()
        return{'FINISHED'}


class BLive_OT_send_osc_message(bpy.types.Operator):
    """
        Operator - send osc message from a string
    """
    bl_idname = "blive.send_osc_message"
    bl_label = "BLive - send OSC message"

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        debug = context.window_manager.blive_debug

        # test if first arg contains '/' (path)
        if debug.message.split(' ')[0].count('/'):
            msg = Message(debug.message.split(' ')[0])
            for i in debug.message.split(' ')[1:]:
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
            return{'FINISHED'}
        else:
            return{'CANCELLED'}

class BLive_OT_connect(bpy.types.Operator):
    bl_idname = "blive.connect"
    bl_label = "BLive connect to gameengine"

    #@classmethod
    #def poll(self, context):
        #pass

    def execute(self, context):
        sc = context.scene
        bc = context.window_manager.blive_settings
        server = bc.server
        port = bc.port
        Client().connect(server, port)
        return{'FINISHED'}

class BLive_OT_disconnect(bpy.types.Operator):
    bl_idname = "blive.disconnect"
    bl_label = "BLive disconnect from gameengine"

    #@classmethod
    #def poll(self, context):
        #pass

    def execute(self, context):
        Client().disconnect()
        return{'FINISHED'}

def register():
    print("settings.ops.register")
    bpy.utils.register_class(BLive_OT_start_gameengine)
    bpy.utils.register_class(BLive_OT_stop_gameengine)
    bpy.utils.register_class(BLive_OT_reload_gameengine)
    bpy.utils.register_class(BLive_OT_save_reload_gameengine)
    bpy.utils.register_class(BLive_OT_restart_gameengine)
    bpy.utils.register_class(BLive_OT_send_osc_message)
    bpy.utils.register_class(BLive_OT_connect)
    bpy.utils.register_class(BLive_OT_disconnect)

def unregister():
    print("settings.ops.unregister")
    bpy.utils.unregister_class(BLive_OT_save_reload_gameengine)
    bpy.utils.unregister_class(BLive_OT_reload_gameengine)
    bpy.utils.unregister_class(BLive_OT_restart_gameengine)
    bpy.utils.unregister_class(BLive_OT_stop_gameengine)
    bpy.utils.unregister_class(BLive_OT_start_gameengine)
    bpy.utils.unregister_class(BLive_OT_send_osc_message)
    bpy.utils.unregister_class(BLive_OT_connect)
    bpy.utils.unregister_class(BLive_OT_disconnect)
