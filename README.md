BLive
=====

Blender addon which allow to control the gameengine from a blender session by using OSC.

The recent development tree needs pyliblo installed. Please look for python-pyliblo or pyliblo
in your package manager. Under windows you have to build pyliblo for yourself.

pyliblo: http://das.nasophon.de/pyliblo/

BLive is tested under Archlinux with blender 2.70. It should be backwards compatible until blender-2.66.


Installation:
=============

First install pyliblo on your system, then install and enable the addon like any other addon. 

_Archlinux:_

yaourt -S python-pyliblo

_Debian:_

TODO
Debian uses an older version of version of blender, with an deprecated python API

_Ubuntu:_

Under 14.04 the addon should work by installing python3-liblo:

apt-get install python3-liblo

_OSX:_

TODO
