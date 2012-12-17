# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# Script copyright (C) 2012 Thomas Achtner (offtools)

def unique_name(collection, name):
	'''
		find a unique name for a new object in a collection
	'''
	def check_name(collection, name, num):
	
		if "{0}.{1}".format(name, str(num).zfill(3)) in collection:
			return check_name(collection, name, num+1)
		return num
	
	if not name in collection:
		return name

	num = check_name(collection, name, 1)
	unique = "{0}.{1}".format(name, str(num).zfill(3))
	return unique
