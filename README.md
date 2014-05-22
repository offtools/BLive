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

_Ubuntu:_

under 14.04 the addon works by installing python3-liblo.

apt-get install python3-liblo

_Debian:_

TODO
Debian uses an older version of version of blender, with an deprecated python API.
With the recent version from blender.org, you need to build pyliblo with the same python
version, that blender uses internally.

_OSX:_

(not tested, just guessed) you can install liblo via macports, also cython is listed there.
Download and build pyliblo, then copy it to your blender installation path under:
BLENDERPATH/scripts/modules/

_Windows_

Building pyliblo under Windows, if someone manages that, please send a pull request :)
http://magic-smoke.blogspot.de/2012/07/building-pyliblo-on-windows-using.html

Usage:
=====

a new tutorial and two example blendfiles are added to the github wiki
