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

#OJO de No agregar python a la lista de instalables, debido a que ya se encuentra instalado
#programas que contiene cada perfil
perfil_basico = ["openjdk-7-jre", "icedtea-7-plugin", "unrar", "p7zip-full", "_ubuntu-restricted-extras", "libreoffice", 
"libreoffice-l10n-es", "_preg_Navegadores","vlc"]
perfil_prog_basico = ['_preg_Editor Texto']
perfil_prog_cpp = ["g++", "_preg_IDEs C++"]
perfil_prog_java = ["openjdk-7-jdk", "openjdk-7-jre", "_preg_IDEs Java"]
perfil_prog_python = ["glade"]
perfil_prog_web = ["lamp-server^", "phpmyadmin","_ruby_rvm","_nodejs"]
perfil_prog_android= ["openjdk-7-jdk", '_preg_IDEs Android']
perfil_comunicacion_basico = ["_skype"]
perfil_diseno_basico = ["openjdk-7-jdk", "openjdk-7-jre", "dia", "mysql-workbench", "_argouml", "_datamodeler", "_evoluspencil", "gimp"]
perfil_redes_basico = ["_wireshark","speedometer"]
perfil_respaldo_basico = ["openjdk-7-jdk", "openjdk-7-jre", "_dropbox", "git", "subversion" ,"_smartgithg"]
perfil_soporte_remoto_basico = ["vino", "vinagre","_teamviewer"]

#diccionario que relaciona el perfil con la lista de software
diccionario_software = {'perfil_basico':perfil_basico,'programacion_basico':perfil_prog_basico,
'comunicacion_basico':perfil_comunicacion_basico,'respaldo':perfil_respaldo_basico,'diseno_basico':perfil_diseno_basico,
'redes':perfil_redes_basico,'soporte_remoto':perfil_soporte_remoto_basico,'programacion_java':perfil_prog_java,
'programacion_cpp':perfil_prog_cpp,'programacion_android':perfil_prog_android, 'programacion_web':perfil_prog_web,
'programacion_python':perfil_prog_python}

navegadores = ['firefox','chromium-browser']
prog_cpp = ['codeblocks', 'qtcreator']
prog_java = ['netbeans','eclipse']
prog_normal = ['_sublimetext','geany']
prog_android = ['_adt_bundle','_android_studio']

diccionario_pref_soft = {'Navegadores':navegadores,'IDEs C++':prog_cpp,'IDEs Java':prog_java, 'Editor Texto':prog_normal,
'IDEs Android':prog_android}


