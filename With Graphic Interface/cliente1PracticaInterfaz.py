from multiprocessing.connection import Client
import time
from time import sleep
from Tkinter import *
import random
from multiprocessing import Queue

from multiprocessing.connection import Listener
from multiprocessing import Process


if __name__ == '__main__':

	#INTERFAZ GRAFICO ----------------------------------------------------------------------------------------------------
	root = Tk()
    	root.title("Whats Up!")    

	queue = Queue()

    	frame = Frame(root)
    	frame.pack()
   
    	contact_number = 5  

	C = 'localhost'
	CH = 'localhost'
	P = 6000
	PC = 6001

	#Nombre Usuario
    	no = Label(frame,text="Nombre")
    	no.grid(row=0, column=0)
    	nu = StringVar()
    	nu.set('nicola')
    	nom = Entry(frame,width=15,textvariable=nu)    
    	nom.grid(row=0, column=1)

	#Password Usuario
    	pa = Label(frame,text="Password")
    	pa.grid(row=0, column=2)
    	pu = StringVar()
    	pu.set('nicola')
    	pas = Entry(frame,width=15,textvariable=pu)    
    	pas.grid(row=0, column=3)

	#IP del server de correos
    	ln = Label(frame,text="IP del server de correos")
    	ln.grid(row=0, column=4)
    	be = StringVar()
    	be.set(C)
    	n = Entry(frame,width=15,textvariable=be)    
    	n.grid(row=0, column=5)

	#PORT del server de correos
    	pc = Label(frame,text="Puerto del server de correos")
    	pc.grid(row=1, column=4)
    	puc = StringVar()
    	puc.set(P)
    	pco = Entry(frame,width=15,textvariable=puc)    
    	pco.grid(row=1, column=5)

	#Nombre Usuario chat
    	noc = Label(frame,text="Nombre")
    	noc.grid(row=4, column=0)
    	nuc = StringVar()
    	nuc.set('nicola')
    	nomc = Entry(frame,width=15,textvariable=nuc)    
    	nomc.grid(row=4, column=1)

	#Password Usuario chat
    	pac = Label(frame,text="Password")
    	pac.grid(row=4, column=2)
    	puch = StringVar()
    	puch.set('nicola')
    	pasc = Entry(frame,width=15,textvariable=puch)    
    	pasc.grid(row=4, column=3)

    	#IP del server de chat
    	ln = Label(frame,text="IP server chat")
    	ln.grid(row=4, column=4)
    	bs = StringVar()
    	bs.set(CH)
    	si = Entry(frame,width=15,textvariable=bs)    
    	si.grid(row=4, column=5)

	#PORT del server de chat
    	pcc = Label(frame,text="Puerto del server de chat")
    	pcc.grid(row=5, column=4)
    	pucc = StringVar()
    	pucc.set(PC)
    	pcoc = Entry(frame,width=15,textvariable=pucc)    
    	pcoc.grid(row=5, column=5)

	def lee_param():       
        	MAIL = n.get()
		CHAT = si.get()
		NOMBRE = nom.get()
		PASS = pas.get()
		PUERTOC = int(pco.get())
		NOMBRECHAT = nomc.get()
		PASSCHAT = pasc.get()
		PUERTOCHAT = int(pcoc.get())
        	return MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT

	def exec_connectcorreos():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
		print 'trying to connect'
		global connM
		connM = Client(address=(MAIL, PUERTOC), authkey='secret password')
		print 'connected'		
		text_mail.insert(END,"\n"+"Connected")
		
	conncorreos_button = Button(frame, text="CONNECT", command=exec_connectcorreos)
	conncorreos_button.grid(row=0, column=6)

	def exec_newuser():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
		connM.send([(NOMBRE,PASS),"new_user",(id,PASS)])
		text_mail.insert(END,"\n"+"Solicitando cuenta.")
		text_mail.insert(END,"\n"+"Cuenta creada?")
		text_mail.insert(END,"\n"+connM.recv())
		
	newuser_button = Button(frame, text="New User", command=exec_newuser)
	newuser_button.grid(row=1, column=0)

	def exec_send_button():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
		a = str(text_mail.get("1.0",END))
		print "sending email with text :", a   
		print "to contacts: ",
		for x in check_contacts:
		    if x.get()==1:
		        print x
			connM.send([(NOMBRE,PASS),"send",(x,a)])
			print connM.recv()
		print "AZZ2"
		
	send_button = Button(frame, text="Send", command=exec_send_button)
	send_button.grid(row=1, column=1)

	def exec_getmail_button():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
		print "getting email from server"
		print "deleting the text_mail content"
		text_mail.delete("1.0",END)                
		print "showing the new messages"
		connM.send([(NOMBRE,PASS),"get_mail"])
		time.sleep(0.5)
		text_mail.insert(END,"\n"+connM.recv())
		
	getmail_button = Button(frame, text="Get Mail", command=exec_getmail_button)
	getmail_button.grid(row=1, column=2)
	   
	def exec_erase_button():
		text_mail.delete("1.0",END)
		print "deleting text area"        
		
	erase_button = Button(frame, text="Erase", command=exec_erase_button)
	erase_button.grid(row=1,column=3)

	#SCROLLBAR MAIL AND TEXT MAIL
	scrollbarmail = Scrollbar(frame)
	scrollbarmail.grid(row=2,column=5)	    
	text_mail = Text(frame,height=10,bg="gray",yscrollcommand=scrollbarmail.set)
	text_mail.grid(row=2, column=0, columnspan=contact_number)
	scrollbarmail.config(command=text_mail.yview)

	def add_contacts():
		print "list of contacts:"
		print check_contacts		

	addcontact_button = Button(frame, text="Creacion Contactos", command=add_contacts)
	addcontact_button.grid(row=1,column=7)

	def exec_check():
		print "list of contacts:"
		for x in check_contacts:
		    print x, "value", x.get()

	check_contacts = []

	for x in range(contact_number):        
		check_contacts.append(IntVar())

	check_buttons = []
	for x in range(contact_number):
		check_buttons.append(Checkbutton(frame, text="contact "+str(x), command=exec_check, variable=check_contacts[x]))        
		check_buttons[x].grid(row=3,column=x)

	local_listener = (('127.0.0.1', 5001),'secret client password')
#	local_listener = (('127.0.0.1', 5001))
	

	#LISTENER CHAT
	def client_listener():
	    cl = Listener(address=local_listener[0], authkey=local_listener[1])
	    print '.............client listener starting' 
	    print '.............accepting conexions'
	    separator = "---------------------------------------------\n"
	    while True:
		conn = cl.accept()
		print '.............connection accepted from', cl.last_accepted
		m = conn.recv()
		print '.............message received from server', m
		queue.put((1,m[0],m[1]))

	#CONNECT CHAT
	def exec_connectchat():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
                print 'trying to connect'
		global connc
    		connc = Client(address=(CHAT, PUERTOCHAT), authkey='secret password server')
#    		connc.send(((1,PASSCHAT),"connect",local_listener))
		connc.send(local_listener)
		#aggiunto client1
		cl = Process(target=client_listener, args=())
    		cl.start() 
		text_chat.insert(END,"\n"+"Connected")
    			
	connchat_button = Button(frame, text="CONNECT", command=exec_connectchat)
	connchat_button.grid(row=4, column=6)

	def exec_sendchat_button():
		MAIL, CHAT, NOMBRE, PASS, PUERTOC, NOMBRECHAT, PASSCHAT, PUERTOCHAT = lee_param()
		separator = "---------------------------------------------\n"
		print "sending chat message:",chat_entry.get()
		connc.send(chat_entry.get())
		print "to contacts: ",
		for x in check_contacts:
		    if x.get()==1:
			connc.send(chat_entry.get())
		        print x,
		print
        	text_chat.insert(END,"\n"+separator+NOMBRECHAT+": "+chat_entry.get())
        
    	sendchat_button = Button(frame, text="Send Chat", command=exec_sendchat_button)
    	sendchat_button.grid(row=6, column=0)

    	chat_entry = Entry(frame,width=80)
	chat_entry.grid(row=6,column=1,columnspan=contact_number)

	scrollbar = Scrollbar(frame)
	scrollbar.grid(row=7,column=5)

    	text_chat = Text(frame,height=10,bg="gray",yscrollcommand=scrollbar.set)
    	text_chat.grid(row=7,column=0,columnspan=contact_number)
	scrollbar.config(command=text_chat.yview)

	def ejec_stop():
		queue.put("quit")

	stop = Button(frame, text="Quit", command=ejec_stop, width=7)
	stop.grid(row=8, column=5)


#INTERFAZ GRAFICO FINE

#        
#	print "chat o correos?"
#	z = raw_input()
#	if z == 'chat':
#		print 'trying to connect'
#    		conn = Client(address=('127.0.0.1', 6001), authkey='secret password server')
#    		conn.send(local_listener)
##aggiunto client1
#
#	    	cl = Process(target=client_listener, args=())
#    		cl.start()
#    
#    		connected = True
##		print "Con quien quieres chatar?"
##		chat = raw_input()
#    		while connected:
#        		value = raw_input("'C', stay connected. 'Q' quit connection \n")
#        		if value == 'Q':
#            			connected = False
#        		else:
#            			print "continue connected"
#            			conn.send(value)
#        
#		print "last message"
#		conn.send("quit")
#		conn.close()
#		cl.terminate()
#		print "end client"
#	
#	elif z == 'correos':
#		print "Donde quieres conectarte?"
#		de = raw_input()
#		print 'trying to connect'
#		#conn = Client(address=('147.96.18.18', 6000), authkey='secret password')
#		conn = Client(address=(de, 6000), authkey='secret password')
#		print 'sending message'
#		print 'Quien eres tu?'
#		a = raw_input()
#		print "Hola,",a
#		print "Cual es tu password?"
#		p = raw_input()
#		bool = True
#		while bool:
#		    print "Que quieres hacer?"
#		    print "- Escribi newuser si quieres crear tu cuenta"
#		    print "- Escribi send si quieres enviar un correo"
#		    print "- Escribi read si quieres leer tu correos"
#		    print "- Escribi quit si quieres terminar la session"
#		    b = raw_input()
#		    if b == 'newuser':
#			conn.send([(a,p),"new_user",(id,p)])
#			print "Solicitando cuenta"
#			print "Cuenta creada?"
#			print conn.recv()
#		    elif b == 'send':
#			print "Escribi el destino del correo"
#			d = raw_input()
#			print "Escribi el message"
#			c = raw_input()
#			conn.send([(a,p),"send",(d,c)])
#			print conn.recv()
#		    elif b == 'read':
#			conn.send([(a,p),"get_mail"])
#			time.sleep(0.5)
#			print "Tus correos son:",conn.recv()
#		    elif b == 'quit':
#			conn.send([(a,p),"quit"])
#			bool = False
##		#print 'received message', conn.recv() 
#		conn.close()
## #When a message is received from server we can change the status of the contacts    
   # #check_contacts[i].set(1) 
   # #check_contacts[i].set(0) 
## 
 ##   	root.mainloop()
	pause = False
    	try:
		while True:
			if not pause:
				if not queue.empty():
					s = queue.get()
					if s == 'quit':
						break
					elif s[0] == 1:
						text_chat.insert(END,"\n---------------------------------------------")
						text_chat.insert(END,"\n"+str(s[2]))
						text_chat.insert(END,": "+str(s[1]))
			root.update()
	except TclError:
		pass
	root.destroy() #elimina la ventana



