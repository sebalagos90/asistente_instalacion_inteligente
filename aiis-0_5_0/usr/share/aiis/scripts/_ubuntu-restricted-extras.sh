#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#Asistente de Instalación Inteligente de Software para distribuciones GNU/Linux basados en Ubuntu 12.04
#Scripts de instalación de software de terceros (fuera de los repositorios oficiales de Ubuntu)
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
    #Solución extraída de http://devrijepc.nl/install/ubuntu-postinstall

export DEBIAN_FRONTEND=noninteractive
/bin/sh -c 'echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections'
sudo apt-get install -qq ttf-mscorefonts-installer && sudo apt-get install -qq ubuntu-restricted-addons && sudo apt-get install -qq gstreamer0.10-plugins-bad-multiverse && sudo apt-get install -qq libavcodec-extra-53 && sudo apt-get install -qq unrar 
exit
