import socket
import threading
import sys
import pickle

class Servidor():
	"""docstring for Servidor"""
	def __init__(self, host = "localhost", port=9000):
		self.clientes = []
		#creacion de el sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#ligamos el socket a el host y al puerto
		self.sock.bind((str(host), int(port)))
		print ("ESPERANDO CONEXIONES EN LOCALHOST, PUERTO:", port)
		#se pueden escuchar 10 conexiones
		self.sock.listen(10)
		self.sock.setblocking(False)
		
		#creacion de los dos hilos uno para aceptar y otro para procesar
		aceptar = threading.Thread(target=self.aceptarCon)
		procesar = threading.Thread(target=self.procesarCon)
		aceptar.daemon = True 
		#los ponemos en ejecucion
		aceptar.start()
		procesar.daemon = True
		#los ponemos en ejecucion
		procesar.start()

		while True:
			msg = input('->')
			if msg == 'salir':
				print("Servidor desconectado") 
				self.sock.close()
				sys.exit()
				
			else:
				pass
		
	
 	 
	#funcion para enviar mensajes atodos los clientes
	def msg_to_all(self, msg, cliente):
		for c in self.clientes:
			try:
				#para que el cliente que envia el mensaje no se debuelva su mismo msj
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)
				 
	
	def aceptarCon(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print("CLIENTE CONECTADO")#Mensaje al cliente conectado
				#para que la conexion no se bloquee
				
				conn.setblocking(False)
				
				#arreglo de clientes 
				self.clientes.append(conn)
			except:
				pass
				
	
		
	#funcio para aceptar las conexiones  
	def procesarCon(self):
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass
		

s = Servidor()
