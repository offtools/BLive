import bpy
import sys
sys.path.append('/usr/lib/python3.2/site-packages')
import liblo

class client(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(client, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self):
        self.target = liblo.Address(9000)
        
    def quit(self):
        liblo.send(self.target, "/quit")
    
    def send(self, path, *args):
    	liblo.send(self.target, path, *args)
        
    def snd_object(self, obj):
        liblo.send(self.target, '/data/objects', obj.name, \
                                            obj.location[0], \
                                            obj.location[1], \
                                            obj.location[2], \
                                            obj.scale[0], \
                                            obj.scale[1], \
                                            obj.scale[2], \
                                            obj.rotation_euler[0], \
                                            obj.rotation_euler[1], \
                                            obj.rotation_euler[2], \
                                            obj.color[0], \
                                            obj.color[1], \
                                            obj.color[2], \
                                            obj.color[3] \
                                            )
                                            
    def cmd_open_video(self, ob, texture, file):
        liblo.send(self.target, '/texture/video/open', ob, texture, file)
        
    def cmd_dummy(self):
    	pass

