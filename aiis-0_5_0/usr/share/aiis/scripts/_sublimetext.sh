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

export DEBIAN_FRONTEND=noninteractive
cd /usr/share/aiis/packages
wget http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2.tar.bz2
mkdir /home/$1/Aplicaciones
tar jvxf Sublime\ Text\ 2.0.2.tar.bz2 -C /home/$1/Aplicaciones
chmod -R 777 /home/$1/Aplicaciones/SublimeText
rm /usr/share/aiis/packages/Sublime\ Text\ 2.0.2.tar.bz2
exit
