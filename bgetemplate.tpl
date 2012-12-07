import sys
import getopt
import types
import bge
from bgeserver import BgeOSCServer

def handle_timeout(self):
	self.timed_out = True

def start():
	'''
		should be called on starting game engine 
	'''
	cont = bge.logic.getCurrentController()
	obj = cont.owner
	port=9900 # --- standard port

	try:
		index = sys.argv.index('-')
		# --- check for additional args (all args after empty '-')
		if len(sys.argv) > index:
			args = sys.argv[index+1:]
			optlist, args = getopt.getopt(args, 'p:', ['port='])
			for o, a in optlist:
				if o in ("-p", "--port"):
					port = int(a)
	except getopt.GetoptError as err:
		print("Error in setting custom options")
		sys.exit()
		
	if not hasattr(bge.logic, 'server'):
		print('OSC Server:', port)
		try:
			bge.logic.server = BgeOSCServer( "127.0.0.1", port )
			print("OSC Server Started", bge.logic.server.address())
		except TypeError as err:
			print('main.py: ', err)
			stop()

def update():
	'''
		general update routine - called each frame
	'''
	if hasattr(bge.logic, 'server'):
		bge.logic.server.update()
