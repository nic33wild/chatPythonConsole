from multiprocessing.connection import Client
import time

print "Donde quieres conectarte?"
de = raw_input()
print 'trying to connect'
#conn = Client(address=('147.96.18.18', 6000), authkey='secret password')
conn = Client(address=(de, 6000), authkey='secret password')
print 'sending message'
print 'Quien eres tu?'
a = raw_input()
print "Hola,",a
print "Cual es tu password?"
p = raw_input()
bool = True
while bool:
    print "Que quieres hacer?"
    print "- Escriba newuser si quieres crear tu cuenta"
    print "- Escriba send si quieres enviar un correo"
    print "- Escriba read si quieres leer tu correos"
    print "- Escriba quit si quieres terminar la session"
    b = raw_input()
    if b == 'newuser':
        conn.send([(a,p),"new user",(id,p)])
        print "Solicitando cuenta"
        print "Cuenta creada?"
        print conn.recv()
    elif b == 'send':
        print "Escribi el destino del correo"
        d = raw_input()
        print "Escribi el message"
        c = raw_input()
        conn.send([(a,p),"send",(d,c)])
        print conn.recv()
    elif b == 'read':
        conn.send([(a,p),"getmail"])
        time.sleep(0.5)
        print "Tus correos son:",conn.recv()
    elif b == 'quit':
        conn.send([(a,p),"quit"])
        bool = False
#print 'received message', conn.recv() 
conn.close()
