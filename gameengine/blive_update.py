import bge

if hasattr(bge.logic, "server"):
	while bge.logic.server.recv(0):
		pass
