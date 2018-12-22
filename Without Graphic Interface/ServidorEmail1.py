from multiprocessing.connection import Listener
from multiprocessing import Manager

print "Cual es tu ip?"
i = raw_input()
listener = Listener(address=(i,6000), authkey='secret password')
print 'listener starting'
manager = Manager()
clientes = manager.list() #Lista de usuarios
password = manager.list() #Lista de usuarios con password
correos = manager.list() #Lista de todos los correos
tcorreos = manager.list() #Lista para enviar los correos de un solo usuario
while True:
    conn = listener.accept()
    bool = True
    print 'Connection accepted from', listener.last_accepted
    while bool:
    	m = conn.recv()
    	print 'Receive message:', m
    	if m[1] == ('new user'):
        	if ((m[0])[0]) not in clientes:
			print "nuevo usuario"
			clientes.append(((m[0])[0]))
                        password.append(m[0])
			conn.send("Si")
			print "CLIENTES:",clientes
		elif ((m[0])[0]) in clientes:
			conn.send("Esto usuario estaba ya registrado")
    	elif m[1] == ('send'):
            	correos.append(m[2])
                conn.send("Correo enviado")
       	    	print "CORREO POR",(m[2])[0],"enviado"
    	elif m[1] == ('getmail'):
            if m[0] in password:                
                for i in range (0,len(correos)):
                    #Creacion lista tcorreos para el invio de los correos
                    if (((m[0])[0]) == (correos[i])[0]):
                        tcorreos.append(correos[i])
                 #Envio lista tcorreos con los correos del usuario
 #               for i in range (0,len(tcorreos)):
 #                   conn.send(tcorreos[i])
                n = str(tcorreos)
                if (n == '[]'):
                    conn.send("No hay correos para ti.")
                else:
                    conn.send(n)
                #Destruccion lista tcorreos
                while (len(tcorreos)) > 0:
                    i = (len(tcorreos)-1)
                    del tcorreos[i]
            else:
                print "password o usuario no correcto"
                conn.send("Password o usuario no correcto")
	elif m[1] == ('quit'):
		bool = False    
   #             conn.send("Adios")
    	else:
        	conn.send("?")
    conn.close()
    print "connection closed"
listener.close()
