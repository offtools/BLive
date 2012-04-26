import server
import bge

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
			bge.logic.server = server.server(port)
		except TypeError as err:
			print('error creating modules')
			stop()

def stop():
	'''
	free osc server context, quit gameengine
	''' 
	if hasattr(bge.logic, 'server'):
		print('received quit, freeing OSC server')
		bge.logic.server.free()
	bge.logic.endGame()

def update():
	'''
	general update routine
	'''
	if hasattr(bge.logic, 'server'):
		bge.logic.server.update()
