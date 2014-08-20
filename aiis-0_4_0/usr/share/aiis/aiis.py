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


from gi.repository import Gtk, GObject
import time
import os
import threading
import re
from funciones import *
from lista_software import diccionario_software
import subprocess

			
class Asistente_Inteligente:  
	
	def __init__(self):
		self.cierreCiclo = False
		self.cajaPrincipal = constructor.get_object("boxVentana")
		self.vista_actual = constructor.get_object("boxPrincipal")
		vent1 = constructor.get_object("boxTerminos")
		vent2 = constructor.get_object("boxPregunta")
		vent3 = constructor.get_object("boxInstalacion")
		vent4 = constructor.get_object("boxFinalizar")
		self.ventanaInstalacion = vent3
		self.ventanaFinalizar = vent4
		img1 = constructor.get_object("imgBienvenida")
		img2 = constructor.get_object("imgTerminos")
		img3 = constructor.get_object("imgUso")
		#img4 = constructor.get_object("imgProgramas") si implemento que muestre la lista de programas a instalar
		img5 = constructor.get_object("imgInstalacion")
		img6 = constructor.get_object("imgFinalizar")
		
		#Lista de las vistas de la interfaz
		self.lista_vistas = [vent1,vent2,vent3,vent4]
		
		#Lista de las imagenes del estado de avance de la interfaz
		self.lista_avance = [img2,img3,img5,img6]
		
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
		
	def ocultarError(self, object, data=None):
		ventana.set_sensitive(True)
		self.ventError.hide()
	
	def siguiente_vista_interno(self):
		print("Cambiando interfaz a la siguiente")
		vista_siguiente = self.lista_vistas.pop(0)
		self.cajaPrincipal.remove(self.vista_actual)
		self.cajaPrincipal.pack_end(vista_siguiente,True,True,5)
		self.vista_actual = vista_siguiente
		self.estado_actual.set_from_stock("gtk-apply",Gtk.IconSize.MENU)
		nuevo_estado = self.lista_avance.pop(0)
		nuevo_estado.set_from_stock("gtk-go-forward",Gtk.IconSize.MENU)
		self.estado_actual = nuevo_estado
		
	def siguiente_vista(self, object, data=None):
		vista_siguiente = self.lista_vistas.pop(0)
		self.cajaPrincipal.remove(self.vista_actual)
		self.cajaPrincipal.pack_end(vista_siguiente,True,True,5)
		self.vista_actual = vista_siguiente
		self.estado_actual.set_from_stock("gtk-apply",Gtk.IconSize.MENU)
		nuevo_estado = self.lista_avance.pop(0)
		nuevo_estado.set_from_stock("gtk-go-forward",Gtk.IconSize.MENU)
		self.estado_actual = nuevo_estado
		
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
				hilo_interfaz = threading.Thread(target=self.siguiente_vista_interno)
				hilo_interfaz.start()
				hilo_interfaz.join()
				hilo_ejecutar = threading.Thread(target=self.instalarProgramas,args=(scripts_necesarios,))
				hilo_ejecutar.start()
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
		
	def instalarProgramas(self,dic_scripts):
		#Extrae las claves de los perfiles seleccionados
		scripts = dic_scripts.keys()
		
		#Solicita la lista con el software a instalar
		lista = self.solicitarSoftware(scripts)
	
		#Actualizando el Sistema para evitar conflictos de versiones y disponibilidad de los paquetes de
		#los respositorios
		self.actualizarSistema()
		
		i = 0
		j = 0.0

		#####		INSTALACION DEL SOFTWARE SELECCIONADO      #######
		fraccion_progreso = 1 / len(lista)
		self.progreso.set_fraction(0.0)
		while(i<len(lista) and not self.cierreCiclo):
			self.estado.set_text("Instalando "+lista[i])
			os.system("export DEBIAN_FRONTEND=noninteractive")
			if(re.search("_[a-z]+",lista[i]) and not self.cierreCiclo):
				#verificando si el paquete está instalado para omitirlo y no desinstalarlo en caso de abortar la instalacion
				if(subprocess.call('dpkg --get-selections | grep '+lista[i][1:],shell=True) == 0):
					lista.pop(i) #se saca el elemento de la lista y no se incrementa el iterador i
				else:
					self.proceso = subprocess.Popen(["/usr/share/aiis/scripts/"+lista[i]+".sh"])
					self.proceso.wait()
					i = i+1

			elif(not self.cierreCiclo):
				#verificando si el paquete está instalado para omitirlo y no desinstalarlo en caso de abortar la instalacion
				if(subprocess.call('dpkg --get-selections | grep '+lista[i],shell=True) == 0):
					lista.pop(i) #se saca el elemento de la lista y no se incrementa el iterador i
				else:
					self.proceso = subprocess.Popen(["sudo","apt-get","install","-y",lista[i]])
					self.proceso.wait()
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
		flags = {"programacion_basico":False,"respaldo":False,"diseno_basico":False,"perfil_basico":False}
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
				self.proceso = subprocess.Popen(["/usr/share/aiis/scripts/des"+lista[k]+".sh"])
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
			
#Esto sería como el main que no hice
constructor = Gtk.Builder()
constructor.add_from_file("/usr/share/aiis/aiis.ui")
constructor.connect_signals(Asistente_Inteligente())
ventana = constructor.get_object("ventanaPrincipal")
ventana.show_all()
#El siguiente código habilita el manejo de hilos, necesario en ubuntu 12.04 (no se necesita en ubuntu 14.04)
GObject.threads_init()
Gtk.main()

