import types
import bge
import OSC
from server import BgeOSCServer
import bgehandler

def handle_timeout(self):
    self.timed_out = True

def start():
	'''
		should be called on starting game engine 
	'''
	cont = bge.logic.getCurrentController()
	obj = cont.owner

	if not hasattr(bge.logic, 'server'):
		port = obj['PORT']
		print('OSC Server:', port)
		try:
			bge.logic.server = BgeOSCServer( "127.0.0.1", port )
			print("OSC Server Started", bge.logic.server.address())			
		except TypeError as err:
			print('main.py: ', err)
			stop()

def stop():
	'''
	free osc server context, quit gameengine
	''' 
	if hasattr(bge.logic, 'server'):
		print('received quit, freeing OSC server')
		bge.logic.server.close()
	bge.logic.endGame()

def update():
	'''
	general update routine
	'''
	if hasattr(bge.logic, 'server'):
		bge.logic.server.update()
