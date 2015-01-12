#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Asistente de Instalación Inteligente de Software para distribuciones GNU/Linux basados en Ubuntu 12.04 a Ubuntu 14.04
    #Copyright (C) <2014>  <Sebastian Nolberto Lagos Gutierrez, slagosgutierrez@gmail.com, Arica, Chile>

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk, GdkPixbuf, GObject
import time
import os
import threading
import re
from funciones import *
from lista_software import diccionario_software, diccionario_pref_soft
import subprocess
import sys

class Asistente_Inteligente:

	def __init__(self):
		self.cierreCiclo = False
		self.cajaPrincipal = constructor.get_object("boxVentana")
		self.vista_actual = constructor.get_object("boxPrincipal")
		vent1 = constructor.get_object("boxTerminos")
		vent2 = constructor.get_object("boxPregunta")
		vent3 = constructor.get_object("boxPreguntaPref")
		vent4 = constructor.get_object("boxInstalacion")
		vent5 = constructor.get_object("boxFinalizar")
		
		self.ventanaPregunaPref = vent3
		self.ventanaInstalacion = vent4
		self.ventanaFinalizar = vent5
		
		img1 = constructor.get_object("imgBienvenida")
		img2 = constructor.get_object("imgTerminos")
		img3 = constructor.get_object("imgUso")
		img4 = constructor.get_object("imgProgramas") 
		img5 = constructor.get_object("imgInstalacion")
		img6 = constructor.get_object("imgFinalizar")

		#Lista de las vistas de la interfaz
		self.lista_vistas = [vent1,vent2,vent3,vent4,vent5]

		#Lista de las imagenes del estado de avance de la interfaz
		self.lista_avance = [img2,img3,img4,img5,img6]

		self.estado_actual = img1
		self.txtRespuesta = constructor.get_object("txtRespuesta")
		self.progreso = constructor.get_object("progressbar")

		#En caso de error
		self.ventError = constructor.get_object("errorDialog")
		self.labelError = constructor.get_object("labelError")
		self.mensajeFinal = constructor.get_object("mensajeFinal")
		self.dialogoConfirmacion = constructor.get_object("dialogoConfirmacion")
		self.mensajeConfirmacion = constructor.get_object("labelConfirmacion")
		self.mensajeInstalacion = constructor.get_object("mensajeInstalacion")
		self.estado = constructor.get_object("estadoInstalacion")
		
		#Definiendo los componentes de la vista de preguntas
		self.listStore = constructor.get_object("listaSoftware")
		self.vistaArbol = constructor.get_object("vistaArbol")
		self.listaPreguntas = []
		self.listaSoftwareInstalar = []
				
	def ocultarError(self, object, data=None):
		ventana.set_sensitive(True)
		self.ventError.hide()

	def siguiente_vista_interno(self):
		print("Cambiando interfaz a la siguiente internamente")
		vista_siguiente = self.lista_vistas.pop(0)
		self.cajaPrincipal.remove(self.vista_actual)
		self.cajaPrincipal.pack_end(vista_siguiente,True,True,5)
		self.vista_actual = vista_siguiente
		self.estado_actual.set_from_stock("gtk-apply",Gtk.IconSize.MENU)
		nuevo_estado = self.lista_avance.pop(0)
		nuevo_estado.set_from_stock("gtk-go-forward",Gtk.IconSize.MENU)
		self.estado_actual = nuevo_estado
		
		if(vista_siguiente == self.ventanaPregunaPref and len(self.listaPreguntas) !=0):
			print("vista siguiente es pregunta pref")
			self.cargarDatosListaPref()
		elif(vista_siguiente == self.ventanaPregunaPref and len(self.listaPreguntas) ==0):
			vista_siguiente = self.lista_vistas.pop(0)
			self.cajaPrincipal.remove(self.vista_actual)
			self.cajaPrincipal.pack_end(vista_siguiente,True,True,5)
			self.vista_actual = vista_siguiente
			self.estado_actual.set_from_stock("gtk-apply",Gtk.IconSize.MENU)
			nuevo_estado = self.lista_avance.pop(0)
			nuevo_estado.set_from_stock("gtk-go-forward",Gtk.IconSize.MENU)
			self.estado_actual = nuevo_estado

		
		if(vista_siguiente == self.ventanaInstalacion):
			hilo_interfaz = threading.Thread(target=self.instalarSoftware)
			hilo_interfaz.start()

	def siguiente_vista(self, object, data=None):
		vista_siguiente = self.lista_vistas.pop(0)
		self.cajaPrincipal.remove(self.vista_actual)
		self.cajaPrincipal.pack_end(vista_siguiente,True,True,5)
		self.vista_actual = vista_siguiente
		self.estado_actual.set_from_stock("gtk-apply",Gtk.IconSize.MENU)
		nuevo_estado = self.lista_avance.pop(0)
		nuevo_estado.set_from_stock("gtk-go-forward",Gtk.IconSize.MENU)
		self.estado_actual = nuevo_estado

	def siguiente_pregunta(self, object, data=None):
		i=0
		while(i<self.cantActualPregunta):
			if(self.listStore[i][0]):
				self.listaSoftwareInstalar.append(self.listStore[i][2])
			i=i+1
		self.cargarDatosListaPref()
		
	def on_clic_instalar(self, widget):
		buffer_texto = self.txtRespuesta.get_buffer()
		start = buffer_texto.get_start_iter()
		end = buffer_texto.get_end_iter()
		texto = buffer_texto.get_text(start,end,False)
		if(texto != ""):
			lista = filtrar(texto)
			scripts_necesarios = analizar(lista)
			if(len(scripts_necesarios) == 0):
				self.labelError.set_text("Por favor, responda a la pregunta o ingrese más información")
				self.ventError.show()
				ventana.set_sensitive(False)
			else:
				#aqui modifiqué el orden del ejecutar con la interfaz, ya que primero hace un análisis y luego debe cargar los datos
				hilo_ejecutar = threading.Thread(target=self.procesoInstalacion,args=(scripts_necesarios,))
				hilo_ejecutar.start()
				hilo_ejecutar.join()
				#~ self.procesoInstalacion(scripts_necesarios)
				hilo_interfaz = threading.Thread(target=self.siguiente_vista_interno)
				hilo_interfaz.start()
				hilo_interfaz.join()	
				
		else:
			self.labelError.set_text("Por favor, responda a la pregunta o ingrese más información")
			self.ventError.show()
			ventana.set_sensitive(False)

	def on_btnAbortar_clicked(self, object, data=None):
		ventana.set_sensitive(False)
		if(self.vista_actual == self.ventanaInstalacion):
			self.mensajeConfirmacion.set_text("¿Está seguro que desea abortar la instalación?")
			self.dialogoConfirmacion.show()
		elif(self.vista_actual != self.ventanaFinalizar):
			self.mensajeConfirmacion.set_text("¿Está seguro que desea salir del asistente?")
			self.dialogoConfirmacion.show()
		else:
			Gtk.main_quit()
		return True

	def on_btnConfirmacionNo_clicked(self, object, data=None):
		self.dialogoConfirmacion.hide()
		ventana.set_sensitive(True)

	def on_btnConfirmacionSi_clicked(self, object, data=None):
		if(self.vista_actual == self.ventanaInstalacion):
			self.cancelarInstalacion()
			self.dialogoConfirmacion.hide()
		else:
			Gtk.main_quit()

		return True

	def gtk_quit(self,object):
		Gtk.main_quit()

	def cargarDatosListaPref(self):
		if(len(self.listaPreguntas)==0):
			print("No hay preguntas")
			self.siguiente_vista_interno()
			#~ hilo_interfaz = threading.Thread(target=self.siguiente_vista_interno)
			#~ hilo_interfaz.start()
			#~ hilo_interfaz.join()
		else:
			print("Limpiando Lista")
			#Limpiar la lista
			self.listStore.clear()
			self.eliminarColumnas()
			aux = diccionario_pref_soft[self.listaPreguntas.pop(0)]
			self.cantActualPregunta = len(aux)
			#añadir los elementos a mostrar en la lista
			for elemento in aux:
				print("Elemento "+elemento)
				if(elemento == aux[0]):
					self.listStore.append([True, GdkPixbuf.Pixbuf.new_from_file_at_size('/usr/share/aiis/iconos/'+elemento+'.png',45,45), elemento])
				else:
					self.listStore.append([False, GdkPixbuf.Pixbuf.new_from_file_at_size('/usr/share/aiis/iconos/'+elemento+'.png',45,45), elemento])
			print("Generando lista")
			render_toggle = Gtk.CellRendererToggle()
			#~ #Se conecta con el evento a implementar "on_cell_toggled" y se gatilla cuando se presiona sobre el checkbox
			render_toggle.connect("toggled", self.on_cell_toggled)
			
			#Se crea la columna de checkboxes o toggles
			columna_toggle = Gtk.TreeViewColumn("Seleccion", render_toggle, active=0) #El numero indica la posicion del elemento
			#en este caso es la primera posicion
			
			#Se añade la columna al arbol o vista o treeView
			self.vistaArbol.append_column(columna_toggle)
			
			#Armando la columna con imagenes
			render_imagenes = Gtk.CellRendererPixbuf()
			columna_imagen = Gtk.TreeViewColumn("Icono", render_imagenes, pixbuf=1)
			self.vistaArbol.append_column(columna_imagen)
			
			#Armando la columna de nombre del software
			nombre_programas = Gtk.CellRendererText()
			columna_programas = Gtk.TreeViewColumn("Programa", nombre_programas, text=2) #Segunda posicion en la interfaz
			
			#Agregando la columna al arbol
			self.vistaArbol.append_column(columna_programas)
			print("ListaGenerada")
		
		return True
	
	def on_cell_toggled(self,widget,path):
		#~ CANT_ELEMENTOS = self.cantActualPregunta #debe ser calculado
		#~ i=0
		#~ print(path)
		#~ #El numero 3 debe reemplazarse por la cantidad de elementos de la lista menos 1
		#~ if(path==str(CANT_ELEMENTOS-1)):
			#~ if(not self.listStore[path][0]):
				#~ while(i<int(path)):
					#~ print(self.listStore[i][0])
					#~ self.listStore[i][0] = False
					#~ i=i+1
			#~ self.listStore[path][0] = not self.listStore[path][0]
			#~ 
		#~ else:
			#~ self.listStore[CANT_ELEMENTOS-1][0] = False
		self.listStore[path][0]= not self.listStore[path][0]
	
	def procesoInstalacion(self,dic_scripts):
		#Extrae las claves de los perfiles seleccionados
		scripts = dic_scripts.keys()

		#Solicita la lista con el software a instalar
		self.listaSoftwareInstalar = self.solicitarSoftware(scripts)
		
		self.listaPreguntas = self.crearListaPreferencias()
		print("Lista Preguntas")
		print(self.listaPreguntas)
		return

	def instalarSoftware(self):
		#~ #Actualizando el Sistema para evitar conflictos de versiones y disponibilidad de los paquetes de
		#~ #los respositorios
		#~ 
		os.system("mkdir /usr/share/aiis/packages")
		self.actualizarSistema()
		lista = self.listaSoftwareInstalar
		i = 0
		j = 0.0

		#####		INSTALACION DEL SOFTWARE SELECCIONADO      #######
		fraccion_progreso = 1 / len(lista)
		self.progreso.set_fraction(0.0)
		while(i<len(lista) and not self.cierreCiclo):
			if(re.search("_[a-z]+",lista[i]) and not self.cierreCiclo):
				self.estado.set_text("Instalando "+lista[i][1:])
				#verificando si el paquete está instalado para omitirlo y no desinstalarlo en caso de abortar la instalacion
				if(subprocess.call('dpkg --get-selections | grep '+lista[i][1:],shell=True) == 0):
					lista.pop(i) #se saca el elemento de la lista y no se incrementa el iterador i
				else:
					self.proceso = subprocess.Popen(["/usr/share/aiis/scripts/"+lista[i]+".sh",USER_NAME])
					self.proceso.wait()
					i = i+1

			elif(not self.cierreCiclo):
				self.estado.set_text("Instalando "+lista[i])
				#verificando si el paquete está instalado para omitirlo y no desinstalarlo en caso de abortar la instalacion
				if(subprocess.call('dpkg --get-selections | grep '+lista[i],shell=True) == 0):
					lista.pop(i) #se saca el elemento de la lista y no se incrementa el iterador i
				else:
					if(subprocess.call('apt-get install -q -y '+lista[i],shell=True) != 0):
						print("Error al instalar "+lista[i])
					
					i = i+1

			j = j + fraccion_progreso
			self.progreso.set_fraction(j)


		#####		DESINSTALACION DE SOFTWARE SI SE ABORTA LA OPERACION		#####

		#en el caso de que hayan abortado la instalacion
		#el asistente desinstalará todo el software instalado
		if(self.cierreCiclo and i > 0):
			self.desinstalarSoftware(lista,i)

		ventana.set_sensitive(True)
		self.siguiente_vista_interno()
		print("Programa terminado")
		return
		
	def crearListaPreferencias(self):
		resultado = []
		i = 0
		print("Estoy en crearListaPreferencias")
		print(self.listaSoftwareInstalar)
		while(i<len(self.listaSoftwareInstalar)):
			if(re.search("\A_preg_.*",self.listaSoftwareInstalar[i])):
				print("Estoy dentro del if")
				elemento = self.listaSoftwareInstalar.pop(i)
				print(elemento)
				resultado.append(elemento[6:])
			else:
				i= i+1
		return resultado
		
	def cancelarInstalacion(self):
		self.mensajeInstalacion.set_text("Deshaciendo cambios, por favor espere")
		self.mensajeFinal.set_text("Error: Proceso abortado por el usuario")
		self.cierreCiclo = True
		#parando los procesos en segundo plano
		self.proceso.kill()
		os.system("sudo pkill -9 wget")
		os.system("sudo pkill -9 apt")

	def actualizarSistema(self):
		#Actualizando repositorios del sistema

		self.estado.set_text("Actualizando los repositorios del sistema ... ")
		self.proceso = subprocess.Popen(["sudo","apt-get","update"])
		self.proceso.wait()
		self.progreso.set_fraction(0.5)

		#Actualizando el sistema
		self.estado.set_text("Actualizando el sistema. Por favor espere ... ")
		self.proceso = subprocess.Popen(["sudo","apt-get","upgrade","-y"])
		self.proceso.wait()
		self.progreso.set_fraction(1.0)
		return

	def solicitarSoftware(self,scripts):
		flags = {'perfil_basico':False,'programacion_basico':False,'comunicacion_basico':False,'respaldo':False,
		'diseno_basico':False,'ingeniero_software':False,'redes':False,'soporte_remoto':False,'programacion_java':False,
		'programacion_cpp':False,'programacion_web':False,'programacion_python':False,'programacion_android':False}
		#flags = {"programacion_basico":False,"respaldo":False,"diseno_basico":False,"perfil_basico":False}
		lista = []
		for scr in scripts :
			if(re.search("programacion_[a-z]+",scr) and scr != "programacion_basico"):
				if(not flags["programacion_basico"]):
					lista = lista + diccionario_software["programacion_basico"]
					flags["programacion_basico"] = True
				lista = lista + diccionario_software[scr]
				flags[scr]=True

			elif(scr == "ingeniero_software"):
				listaAuxiliar = ["respaldo","diseno_basico","perfil_basico"]
				for aux in listaAuxiliar :
					if(not flags[aux]):
						#print("Añadiendo "+aux+" y estoy dentro de ing software")
						lista = lista + diccionario_software[aux]
						flags[aux] = True
			else:
				if(not flags[scr]):
					print("Añadiendo "+scr)
					lista = lista + diccionario_software[scr]
					flags[scr]=True

		return lista

	def desinstalarSoftware(self,lista,i):
		print("Se ha interrumpido la instalación, desinstalando software...")

		#Por si se estaban instalando paquetes y quedó la creme de la creme
		self.proceso = subprocess.Popen(["sudo","pkill","-9","wget"])
		self.proceso.wait()

		self.proceso = subprocess.Popen(["sudo","pkill","-9","apt"])
		self.proceso.wait()
		#En caso de que este programa no suelte a apt, entonces lo obligamos eliminando los locks

		os.system("sudo rm /var/lib/dpkg/lock")
		os.system("sudo rm /var/cache/apt/archives/lock")

		#Reparando paquetes rotos o instalaciones a medias
		os.system("sudo dpkg --configure -a")
		os.system("sudo apt-get autoremove -y")
		#cambiar mensaje en la vista de instalacion
		k = 0
		j = 1.0
		fraccion_progreso = 1 / i

		while(k<i):
			self.estado.set_text("Desinstalando "+lista[k])
			os.system("export DEBIAN_FRONTEND=noninteractive")
			if(re.search("_[a-z]+",lista[k])):
				self.proceso = subprocess.Popen(["/usr/share/aiis/scripts/des"+lista[k]+".sh",USER_NAME])
				self.proceso.wait()
			else:
				self.proceso = subprocess.Popen(["sudo","apt-get", "remove","-y",lista[k]])
				self.proceso.wait()

			j = j - fraccion_progreso
			k = k+1
			self.progreso.set_fraction(j)

		#Eliminando paquetes huerfanos para limpiar el sistema
		self.proceso = subprocess.Popen(["sudo","apt-get", "autoremove","-y"])
		self.proceso.wait()

	def eliminarColumnas(self):
		lista_columnas = self.vistaArbol.get_columns()
		for elemento in lista_columnas:
			self.vistaArbol.remove_column(elemento)
		
		
#Esto sería como el main que no hice
#Esto sirve para pasar el user name antes de ejecutar la app con gksu
USER_NAME = sys.argv[1]
print("Hola soy "+USER_NAME)
constructor = Gtk.Builder()
constructor.add_from_file("/usr/share/aiis/aiis.ui")
constructor.connect_signals(Asistente_Inteligente())
ventana = constructor.get_object("ventanaPrincipal")
ventana.show_all()
#El siguiente código habilita el manejo de hilos, necesario en ubuntu 12.04 (no se necesita en ubuntu 14.04)
GObject.threads_init()
Gtk.main()
