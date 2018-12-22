#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import cPickle as p

class AddressBook:

        email = {}
        inputt = ''
        archivo = 'ab.data'

        def __init__(self): # decidiendo si es necesario cargar o crear ab.data
                try:
                        f = file(AddressBook.archivo)
                        AddressBook.email = p.load(f)
                        f.close()
                except:
                        f = file(AddressBook.archivo,'w')
                        f.close()

                print '---------------------------------------'
                print ' AddressBook 1.0'
                print '---------------------------------------'

        def menu(self):
                while not ('a'<= AddressBook.inputt <='f'):
                        print 'a) Agregar contacto'
                        print 'b) Modificar Contacto'
                        print 'c) Eliminar contacto'
                        print 'd) Buscar contacto'
                        print 'e) Mostrar todos'
                        print 'f) Salir'
            
                        AddressBook.inputt = raw_input('ingrese una opción: ')
            
                        if not ('a'<= AddressBook.inputt <='f'):
                                print '---------------------------------------'
                                print 'La opción "%s" no es correcta' % AddressBook.inputt
                                print '---------------------------------------'

        def add(self): # agregar contacto
                contact = raw_input('Ingrese el nombre del contacto: ')
                email = raw_input('Ingrese email: ')
                AddressBook.email[contact] = email
		print AddressBook,"AAAAAAAAAAZZZZZZZ"
		print AddressBook.email
		print AddressBook.email[contact]
		print email	
                print '---------------------------------------'
                print '"%s" ha sido agregado(a)' % contact
                print '---------------------------------------'

                AddressBook.inputt = ''
        
        def modify(self): # modificar contacto
                contact = raw_input('Ingrese el contacto que desea modificar: ')

                if contact in AddressBook.email:
                        email = raw_input('ingrese el nuevo email: ')
                        AddressBook.email[contact] = email
                        print '---------------------------------------'
                        print '"%s" ha sido actualizado(a)' % contact
                        print '---------------------------------------'
                else:
                        print '---------------------------------------'
                        print '"%s" no existe' % contact
                        print '---------------------------------------'

                AddressBook.inputt = ''
        
        def delete(self): # eliminar contacto
                contact = raw_input('Ingrese el contacto que desea eliminar: ')

                if contact in AddressBook.email:
                        del AddressBook.email[contact]
                        print '---------------------------------------'
                        print '"%s" ha sido eliminado(a)' % contact
                        print '---------------------------------------'
                else:
                        print '---------------------------------------'
                        print '"%s" no existe(a)' % contact
                        print '---------------------------------------'
            
                AddressBook.inputt = ''

        def search(self): # buscar contacto
                contact = raw_input('Ingrese el nombre del contacto: ')

                if contact in AddressBook.email:
                        print '---------------------------------------'
                        print 'El email de %s es %s' % (contact, AddressBook.email[contact])
                        print '---------------------------------------'

                else:
                        print '---------------------------------------'
                        print '"%s" no existe' % contact
                        print '---------------------------------------'
            
                AddressBook.inputt = ''

        def view_all(self): # mostrar todos los contactos
                print '---------------------------------------'
                for name, email in AddressBook.email.items():
                        print 'El email de %s es %s' % (name,email)
                        print '---------------------------------------'


                AddressBook.inputt = ''

# programa principal
a = AddressBook()
a.menu()

while a.inputt != 'f':
        if a.inputt == 'a':
                a.add()
                a.menu()
    
        elif a.inputt == 'b':
                a.modify()
                a.menu()
    
        elif a.inputt == 'c':
                a.delete()
                a.menu()

        elif a.inputt == 'd':
                a.search()
                a.menu()
        
        elif a.inputt == 'e':
                a.view_all()
                a.menu()

if a.inputt == 'f': # guardar los contactos en un archivo
        f = file(a.archivo,'w')
        p.dump(a.email,f)
        f.close()
