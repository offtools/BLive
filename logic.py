import bpy
import os

#
#  Operator - creates gamelogic used by osc server in gameengine
#
class BLive_OT_logic_add(bpy.types.Operator):
    bl_idname = "blive.logic_add"
    bl_label = "BLive - create logic brick"
    port = bpy.props.IntProperty(default=9000)

    def execute(self, context):
        if not 'main.py' in bpy.data.texts:
            self.add_script()
        self.add_gamelogic(context)
        return{'FINISHED'} 

    def add_gamelogic(self, context):
        '''
            create gamelogic bricks 
        '''
        bpy.ops.object.select_camera()
        
        if not 's.init' in context.scene.camera.game.sensors:
            bpy.ops.logic.sensor_add(type='ALWAYS', name='s.init')
        context.scene.camera.game.sensors['s.init'].use_pulse_true_level = False
        context.scene.camera.game.sensors['s.init'].use_pulse_false_level = False
        
        if not 's.update' in context.scene.camera.game.sensors:
            bpy.ops.logic.sensor_add(type='ALWAYS', name='s.update')
        context.scene.camera.game.sensors['s.update'].use_pulse_true_level = True
        context.scene.camera.game.sensors['s.update'].use_pulse_false_level = False
        context.scene.camera.game.sensors['s.update'].frequency = 0
    
        if not 'c.init' in context.scene.camera.game.controllers:
            bpy.ops.logic.controller_add(type='PYTHON', name='c.init')       
        context.scene.camera.game.controllers['c.init'].mode = 'MODULE'
        context.scene.camera.game.controllers['c.init'].module = "main.start"
    
        if not 'c.update' in context.scene.camera.game.controllers:
            bpy.ops.logic.controller_add(type='PYTHON', name='c.update')       
        context.scene.camera.game.controllers['c.update'].mode = 'MODULE'
        context.scene.camera.game.controllers['c.update'].module = "main.update"
        
        context.scene.camera.game.sensors['s.init'].link(context.scene.camera.game.controllers['c.init'])    
        context.scene.camera.game.sensors['s.update'].link(context.scene.camera.game.controllers['c.update'])
    
        if not 'PORT' in context.scene.camera.game.properties:
            bpy.ops.object.game_property_new(type='INT', name='PORT')
        context.scene.camera.game.properties['PORT'].value = self.port

    def add_script(self):
        '''
            add server script for bge, appends import path dynamicly
        '''
        print("add bge init script")
        filename = "main.py"
        tpl = "bge_template.tpl"
        paths = bpy.utils.script_paths()
        for i in paths:
            path = os.path.join(i, "addons")
            for j in bpy.path.module_names(path, True):
                if "blive" in j[0]:
                    bpy.data.texts.new(name=filename)
                    
                    directory = os.path.dirname(j[1])
                    filepath = os.path.join(directory, tpl)
                    file = open(filepath, 'r')
                    
                    # add import path
                    textblock = bpy.data.texts[filename] 
                    textblock.write("import sys\n")
                    textblock.write("sys.path.append('{0}')\n".format(directory))

                    for line in file:
                        textblock.write(line)
                    file.close()
                    return

#
#  Operator - removes the logic brick from active camera
#

class BLive_OT_logic_remove(bpy.types.Operator):        
    bl_idname = "blive.logic_remove"
    bl_label = "BLive - remove logic brick"
    
    def execute(self, context):
        bpy.ops.object.select_camera()
        name = bpy.context.scene.camera.name
        
        if "s.init" in context.scene.camera.game.sensors:
            bpy.ops.logic.sensor_remove(sensor="s.init", object=name)
        
        if "s.update" in context.scene.camera.game.sensors:
            bpy.ops.logic.sensor_remove(sensor="s.update", object=name)
    
        if "c.init" in context.scene.camera.game.controllers:
            bpy.ops.logic.controller_remove(controller="c.init", object=name)
    
        if "c.update" in context.scene.camera.game.controllers:
            bpy.ops.logic.controller_remove(controller="c.update", object=name)
    
        if "PORT" in context.scene.camera.game.properties:
            idx = bpy.context.scene.camera.game.properties.keys().index("PORT")
            bpy.ops.object.game_property_remove(index=0)
                   
        return{'FINISHED'}
