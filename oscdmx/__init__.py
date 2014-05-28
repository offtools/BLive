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

# import modules
if "bpy" in locals():
    print("imp.reload")
    import imp
    imp.reload(props)
    imp.reload(ops)
    imp.reload(ui)

else:
    from . import props
    from . import ops
    from . import ui
    pass

def register():
    print("oscdmx.register")
    props.register()
    ops.register()
    ui.register()

def unregister():
    print("oscdmx.unregister")
    ui.unregister()
    ops.unregister()
    props.unregister()
