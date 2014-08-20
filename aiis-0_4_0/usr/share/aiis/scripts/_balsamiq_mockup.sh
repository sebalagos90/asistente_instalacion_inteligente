#!/bin/bash
# -*- ENCODING: UTF-8 -*-

#Asistente de Instalación Inteligente de Software para distribuciones GNU/Linux basados en Ubuntu 14.04
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
#Instalando dependencias del balsamiq mockup
sudo apt-get install ia32-libs-multiarch -y # Note: This dep is a bit overkill but it's useful anyway
ln -s /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0

cd /usr/share/aiis/packages
test ! -f /usr/share/aiis/packages/AdobeAIRInstaller.bin && wget http://airdownload.adobe.com/air/lin/download/2.6/AdobeAIRInstaller.bin
test ! -f /usr/share/aiis/packages/MockupsForDesktop32bit.deb && wget http://builds.balsamiq.com/b/mockups-desktop/MockupsForDesktop32bit.deb
#Instalando Adobe Air
sudo chmod +x /usr/share/aiis/packages/AdobeAIRInstaller.bin
sudo /usr/share/aiis/packages/AdobeAIRInstaller.bin -silent -eulaAccepted

#Instalando Balsamiq Mockup
sudo dpkg -i /usr/share/aiis/packages/MockupsForDesktop32bit.deb
exit 
