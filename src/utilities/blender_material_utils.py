# Stinkefurz
#
# Stinkefurz fork website : https://github.com/AntjeRocks/stinkefurz
#
# Portions of this code are derived from the MB-Lab project:
# https://github.com/animate1978/MB-Lab
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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
#
# ManuelbastioniLAB - Copyright (C) 2015-2018 Manuel Bastioni

import bpy

from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def swap_material(character, old_material_name, new_material_name):
    log.info(f"Swap material from: {old_material_name} to: {new_material_name}")

    if _material_exists(old_material_name) and _material_exists(new_material_name):
        old_material = bpy.data.materials[old_material_name]
        new_material = bpy.data.materials[new_material_name]

        for i in range(0, len(character.data.materials)):
            if character.data.materials[i] == old_material:
                character.data.materials[i] = new_material
    else:
        log.error("Materials weren't found")
        raise ValueError("Error while swapping materials, at least one material wasn't found.")


def _material_exists(material_name):
    return material_name in bpy.data.materials
