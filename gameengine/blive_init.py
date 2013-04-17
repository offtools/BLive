import getopt
import bge
from gameengine import libloserver


SERVER = '127.0.0.1'
PORT = 9901

try:
	index = sys.argv.index('-')

	# --- check for port argument (all args after empty '-')
	if len(sys.argv) > index:
		args = sys.argv[index+1:]
		optlist, args = getopt.getopt(args, 'p:', ['port='])
		for o, a in optlist:
			if o in ("-p", "--port"):
				PORT = int(a)

except getopt.GetoptError as err:
	print("Error in setting Port using"%PORT)

libloserver.Init(PORT)
