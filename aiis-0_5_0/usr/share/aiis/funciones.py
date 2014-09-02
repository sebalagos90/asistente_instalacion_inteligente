#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Asistente de Instalación Inteligente de Software para distribuciones GNU/Linux basados en Ubuntu 12.04
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

from unicodedata import normalize
import re

#Funciones del asistente, todas retornan datos

def eliminarAcentos(txt):
	return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')

#Eliminacion de conectores listo
def eliminarConectores(texto):
	print("Eliminando conectores")
	lista = texto.split()
	listaConectores = ['yo','ademas','mis','a','para','ya','sea','o','y','de','con','mi','e','otros','etc','ver','otras','aunque','la','eso','por','lo','en','tambien']
	i=0
	while(i<len(listaConectores)):
		while(True):
			try:
				lista.remove(listaConectores[i])
				print(listaConectores[i])
			except:
				break
		i=i+1

	return lista

#Eliminacion de caracteres especiales listo
def eliminarCaractEsp(texto):
	print("Eliminando caracteres especiales")
	i=0
	while(i<len(texto)):
		if re.search("[^a-z]",texto[i]) and texto[i] != "+" and texto[i] != " ":
			print(texto[i])
			texto = texto[:i] + texto[(i+1):] #elimina el caracter mediante una concatenacion
		else:
			i = i+1
	return texto

#filtrar listo
def filtrar(texto):
	texto = eliminarAcentos(texto)
	texto = texto.lower()
	texto = eliminarCaractEsp(texto)
	lista = eliminarConectores(texto)
	return lista

#Creacion de diccionario lista
def crear_diccionario():
	basico = ['estudiar','estudio','trabajar','trabajo','informes','documentos','universidad','navegar','internet']
	prog_basico = ['programacion','programar']
	comunicacion = ['comunicacion','comunicarme','conferencias','conferencia']
	respaldo = ['respaldar','almacenamiento','versionado','respaldo']
	disenador = ['diseno', 'disenos','disenado','modelado','modelos','modelar','disenar']
	ing_software = ['ingenieria','desarrollo','desarrollar']
	redes = ['redes','trafico','red']
	soporte_remoto = ['soporte','remoto','vnc']
	prog_java = ['java','applets','applet']
	prog_cpp = ['c','cpp','c++']
	prog_web = ['web','rails','ruby']
	prog_python = ['python']
	prog_android = ['android','movil','moviles']
	lista_palabras = [basico,prog_basico,comunicacion,respaldo,disenador,ing_software,redes,soporte_remoto,prog_java,prog_cpp,prog_web,prog_python, prog_android]

	perfiles = ['perfil_basico','programacion_basico','comunicacion_basico','respaldo','diseno_basico','ingeniero_software','redes','soporte_remoto','programacion_java','programacion_cpp','programacion_web','programacion_python','programacion_android']

	i = 0
	j = 0
	diccionario_palabras = {}
	while(i< len(perfiles)):
		while(j<len(lista_palabras[i])):
			diccionario_palabras[lista_palabras[i][j]] = perfiles[i]
			#print(diccionario_palabras)
			j = j+1
		i = i+1
		j = 0
	#print("Diccionario Palabras: ",diccionario_palabras)
	return diccionario_palabras

#Analiza palabra por palabra comparándola con las claves del diccionario
def analizar(lista):
	diccionario = crear_diccionario()
	i = 0
	diccionario_perfiles = {}
	while(i<len(lista)):
		if(lista[i] in diccionario):
			#Si está en el diccionario, se debe marca verdadero en el diccionario del perfil
			diccionario_perfiles[diccionario[lista[i]]] = True
			print("La palabra: ",lista[i]," pertenece al perfil: ",diccionario[lista[i]])
		#else:
		#	print("La palabra: ",lista[i]," no está en el diccionario")
		i = i+1

	return diccionario_perfiles
