import socket
import threading
import sys
import pickle

#creamos una clase para el cliente
class Cliente():
	"""docstring for Cliente"""
	def __init__(self, host="localhost", port=9000):
		
		#variable para almacenar el socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#conexion con el servidor
		self.sock.connect((str(host), int(port)))
		
		
		#hilo para recivir los mensajes, 
		msg_recv = threading.Thread(target=self.msg_recv)
		#se usa daemon para que este ligado al hilo principal, y al cerrar el programa este se termine
		msg_recv.daemon = True
		msg_recv.start()
		

		while True:
			#entradad del msj
			msg = input('->')
			if msg != 'salir':
				
				#se encia el msj si es diferente a salir
				self.send_msg(msg)
			else:
				print("Cliente desconectado")
				self.sock.close()
				sys.exit()

	def msg_recv(self):
		while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(pickle.loads(data))
			except:
				pass
	#funcion para enviar un mensaje

	def send_msg(self, msg):
		self.sock.send(pickle.dumps(msg))

#inicialisamoes el cliente
c = Cliente()
		
