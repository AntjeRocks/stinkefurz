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

from utilities.blender_const import MATERIAL_CENSORED_SKIN_NAME, MATERIAL_ANIME_SKIN, MATERIAL_HUMANOID_SKIN
from utilities.blender_material_utils import swap_material
from utilities.blender_utils import get_object_by_name
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def remove_humanoid_censors(character_identifier):
    log.info(f"Remove censors from humanoid: {character_identifier}")
    character = get_object_by_name(character_identifier)
    if character:
        if character_identifier in ("f_an01", "f_an02", "m_an01", "m_an02"):
            swap_material(character, MATERIAL_CENSORED_SKIN_NAME, MATERIAL_ANIME_SKIN)
        else:
            swap_material(character, MATERIAL_CENSORED_SKIN_NAME, MATERIAL_HUMANOID_SKIN)
