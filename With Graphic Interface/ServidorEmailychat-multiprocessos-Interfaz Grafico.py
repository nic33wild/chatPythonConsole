from multiprocessing.connection import Listener
from multiprocessing import Manager
from multiprocessing import Process
from Tkinter import *
import random
from multiprocessing import Queue

from multiprocessing.connection import Client
from time import time

def notify_new_client(id,chatclient): 
    for client, client_info in chatclient.items():
        if not client == id:
            print ("sending new client to", client)
            conn = Client(address=client_info[0], authkey=client_info[1])
            conn.send(("new client", id))
            conn.close()

def send_to_client(id,chatclient,message): 
    for client, client_info in chatclient.items():
	#Togliere la riga dopo per mandarlo anche a se stessi
	#    if client <> id:
	#	print client,"AAAAAAAAAAAAAA",client_info,"BBBBBBBBBBBBBBBBBBB",chatclient.items(),"CCCCCCCCCCCCCCCCCCCCCC",id
            	print ("sending messaje to clients", chatclient)
            	conn = Client(address=client_info[0], authkey=client_info[1])
            	conn.send((message, id))

def notify_quit_client(id,chatclient): 
    for client, client_info in chatclient.items():
            print ("sending quit client to", chatclient)
            conn = Client(address=client_info[0], authkey=client_info[1])
            conn.send(("quit client", id))

def serve_clientchat(conn, id, chatclient):
    connected = True
    while connected:
        try:
            m = conn.recv()
        except EOFError:
            print ('connection abruptly closed by client')
            connected = False
        print ('received message:', m, 'from', id)
        if m == "quit":    
            connected = False
            conn.close() 
    #elif m <> "quit":
        else:
	        send_to_client(id,chatclient,m)
    del chatclient[id]                       
    notify_quit_client(id, chatclient)            
    print (id, 'connection closed')


def serve_client(conn,id,clientes,password,correos):
	while True:
	    bool = True
	    while bool:
	    	m = conn.recv()
	    	print ('Receive message:', m)
	    	if m[1] == ('new_user'):
			    if ((m[0])[0]) not in clientes:
				    print ("nuevo usuario")
				    clientes.append(((m[0])[0]))
                            password.append(m[0])
				    conn.send("Si")
				    print "CLIENTES:",clientes
			    elif ((m[0])[0]) in clientes:
				    conn.send("Esto usuario estaba ya registrado")
	    	elif m[1] == ('send'):
		    	correos.append(((m[0])[0],m[2]))
		        conn.send("Correo enviado")
	       	    	print "CORREO POR",(m[2])[0],"enviado"
	    	elif m[1] == ('get_mail'):
		    if m[0] in password:                
		        for i in range (0,len(correos)):
		            #Creacion lista tcorreos para el invio de los correos
		            if (((m[0])[0]) == (((correos[i])[1])[0])):
		                tcorreos.append(correos[i])
		         #Envio lista tcorreos con los correos del usuario
		        n = str(tcorreos)
		        if (n == '[]'):
		            conn.send("No hay correos para ti.")
		        else:
		            conn.send(n)
		        #Destrucion lista tcorreos
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



if __name__ == '__main__':

	queue = Queue()
	manager = Manager()
	chatclient = manager.dict()
	clientes = manager.list() #List de usuarios correo
	password = manager.list() #List de usuarios con password correo
	correos = manager.list() #List de todos los correos
	tcorreos = manager.list() #List para enviar los correos de un solo usuario

	root = Tk()
    	root.title("Nicotrent - Servidor de email y chat!")    
    
    	frame = Frame(root)
    	frame.pack()   
     
	C = 'localhost'
	CH = 'localhost'
	P = 6000
	PC = 6001

	#Control del IP del server de correos
    	ln = Label(frame,text="IP server correos")
    	ln.grid(row=0, column=0)
    	be = StringVar()
    	be.set(C)
    	n = Entry(frame,width=15,textvariable=be)    
    	n.grid(row=0, column=1)

	#PORT del server de correos
    	pc = Label(frame,text="Puerto server correos")
    	pc.grid(row=0, column=2)
    	puc = StringVar()
    	puc.set(P)
    	pco = Entry(frame,width=6,textvariable=puc)    
    	pco.grid(row=0, column=3)

    	#Control del IP del server de chat
    	ln = Label(frame,text="IP server chat")
    	ln.grid(row=1, column=0)
    	bs = StringVar()
    	bs.set(CH)
    	si = Entry(frame,width=15,textvariable=bs)    
    	si.grid(row=1, column=1)

	#PORT del server de chat
    	pcc = Label(frame,text="Puerto server chat")
    	pcc.grid(row=1, column=2)
    	pucc = StringVar()
    	pucc.set(PC)
    	pcoc = Entry(frame,width=6,textvariable=pucc)    
    	pcoc.grid(row=1, column=3)	

	def lee_param():       
        	MAIL = n.get()
		CHAT = si.get()
		PCORREO	= int(pco.get())	
		PCHAT = int(pcoc.get())
        	return MAIL, CHAT, PCORREO, PCHAT
	

	def exec_chat():
			MAIL, CHAT, PCORREO, PCHAT = lee_param()
			listener = Listener(address=(CHAT, PCHAT), authkey='secret password server')
		    	print 'listener starting'
		    	while True:
				print 'accepting conexions'
				conn = listener.accept()
				print 'connection accepted from', listener.last_accepted
				client_info = conn.recv()
				print client_info
				chatclient[listener.last_accepted] = client_info
				print chatclient[listener.last_accepted]
				print listener.last_accepted
				print chatclient
				print 'azz'					
				notify_new_client(listener.last_accepted, chatclient)
				p = Process(target=serve_clientchat, args=(conn,listener.last_accepted,chatclient))
				p.start()

	def abrir_chat():
			global chatact
			chatact = Process(target=exec_chat, args=())
    		        chatact.start() 

	chat_button = Button(frame, text="Start Chat", command=abrir_chat)
	chat_button.grid(row=1, column=4)

	def cerrar_chat():
			chatact.terminate()
			print 'end server chat'		
		
	cerrar_chat_button = Button(frame, text="Cerrar Chat", command=cerrar_chat)
	cerrar_chat_button.grid(row=1, column=5)

	def exec_correos():
			MAIL, CHAT, PCORREO, PCHAT = lee_param()
			listener = Listener(address=(MAIL,PCORREO), authkey='secret password')
			print 'listener starting'
			while True:
				print 'accepting conexions'
				conn = listener.accept()
				print 'connection accepted from', listener.last_accepted
				p = Process(target=serve_client, args=(conn,listener.last_accepted,clientes,password,correos))
				p.start()

	def abrir_correos():
			global correoact
			correoact = Process(target=exec_correos, args=())
    		        correoact.start() 

	acorreos_button = Button(frame, text="Start Correos", command=abrir_correos)
	acorreos_button.grid(row=0, column=4)
		
	def cerrar_correos():
			correoact.terminate()
			print 'end server correos'
		
	cerrar_correos_button = Button(frame, text="Cerrar Correos", command=cerrar_correos)
	cerrar_correos_button.grid(row=0, column=5)

	def ejec_stop():
		queue.put("quit")

	stop = Button(frame, text="Quit", command=ejec_stop, width=7)
	stop.grid(row=2, column=5)

#	def ejec_pause():
#		global pause
#		pause = True
#		
#        pause = Button(frame, text="Pause", command=ejec_pause, width=7)
#        pause.grid(row=2, column=2)
#
#	def ejec_restart():
#		global pause
#		pause = False
#		
#       restart = Button(frame, text="Restart", command=ejec_pause, width=7)
#       restart.grid(row=2, column=1)




#INTERFAZ GRAFICO FINE

#	pause = False
    	try:
		while True:
#			if not pause:
				if not queue.empty():
					s = queue.get()
					if s == 'quit':
						break
				root.update()
	except TclError:
		pass
	root.destroy() #elimina la ventana
