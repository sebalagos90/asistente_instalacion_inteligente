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
#dependencias Firefox??? que!!!!
sudo apt-get install -qq firefox firefox-locale-es
sudo wget https://evoluspencil.googlecode.com/files/evoluspencil_2.0.5_all.deb
sudo dpkg -i /usr/share/aiis/packages/evoluspencil_2.0.5_all.deb
if [ $? != 0 ]
then 
	echo "Error en la instalacion de evoluspencil, Intentando reinstalar"
	sudo rm /usr/share/aiis/packages/evoluspencil_2.0.5_all.deb
	cd /usr/share/aiis/packages/
	sudo wget https://evoluspencil.googlecode.com/files/evoluspencil_2.0.5_all.deb
	sudo dpkg -i /usr/share/aiis/packages/evoluspencil_2.0.5_all.deb
	if [ $? != 0 ]
	then 
		exit 100
	fi
fi
exit 0
