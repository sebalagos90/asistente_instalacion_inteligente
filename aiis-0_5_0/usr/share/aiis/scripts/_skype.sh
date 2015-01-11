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
#Instalando dependencias de Skype
sudo apt-get install -qq libqt4-dbus libqt4-network libqt4-webkit libqt4-xml libqtcore4 libqtgui4
cd /usr/share/aiis/packages
sudo wget http://download.skype.com/linux/skype-ubuntu-precise_4.3.0.37-1_i386.deb
sudo dpkg -i /usr/share/aiis/packages/skype-ubuntu-precise_4.3.0.37-1_i386.deb
if [ $? != 0 ]
then 
	echo "Error en la instalacion de skype, Intentando reinstalar"
	sudo rm /usr/share/aiis/packages/skype-ubuntu-precise_4.3.0.37-1_i386.deb
	cd /usr/share/aiis/packages/
	sudo wget http://download.skype.com/linux/skype-ubuntu-precise_4.3.0.37-1_i386.deb
	sudo dpkg -i /usr/share/aiis/packages/skype-ubuntu-precise_4.3.0.37-1_i386.deb
	if [ $? != 0 ]
	then 
		exit 100
	fi
fi
exit 0
