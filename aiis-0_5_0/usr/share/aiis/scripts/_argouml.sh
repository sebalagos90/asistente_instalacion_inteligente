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


cd /usr/share/aiis/packages
sudo wget https://www.dropbox.com/s/65b9lpdjr5etvz9/argouml_0.34-1.deb
valor=16407542
descarga=$(stat -c %s /usr/share/aiis/packages/argouml_0.34-1.deb)
if [ "$descarga" == "$valor" ]
then
	sudo dpkg -i /usr/share/aiis/packages/argouml_0.34-1.deb
	exit 0
else
	exit 100
fi

