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

from enums.humanoid_base_model_names import HumanoidBaseModelName
from utilities.assets_const import PATH_TO_HUMANOID_BLENDER_FILE
from utilities.blender_const import COLLECTION_NAME_CHARACTER
from utilities.blender_utils import link_object_to_collection, get_object_by_name
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def import_character_from_humanoid_blender_file(char_import_name: HumanoidBaseModelName, char_saving_name: str):
    """Imports character from 'humanoid.blend' file and links it to the current one and returns the character"""
    if char_import_name:
        log.info(f"Importing character: {char_import_name}")
        character = _get_single_character_from_humanoid_library(char_import_name)
        link_object_to_collection(character, COLLECTION_NAME_CHARACTER)
        imported_char = get_object_by_name(char_import_name)
        if imported_char:
            if char_saving_name:
                log.info(f"Renaming: {char_import_name} to: {char_saving_name}")
                imported_char.name = char_saving_name
                return imported_char
            else:
                return imported_char
        else:
            log.error(f"No character with the name: {char_import_name} was imported")
            raise ValueError(
                f"Character: {char_import_name} couldn't be found in the {PATH_TO_HUMANOID_BLENDER_FILE} file")
    else:
        log.error("No character_name was given.")
        raise ValueError("No character_name was given, can not proceed.")


def _get_single_character_from_humanoid_library(character_name):
    """
    Searches for characters from 'humanoid.blend' file with given character_name,
    throws exception if more than one character was found,
    returns one single character
    """
    log.info(f"Searching for: {character_name} in: {PATH_TO_HUMANOID_BLENDER_FILE}")
    try:
        with bpy.data.libraries.load(PATH_TO_HUMANOID_BLENDER_FILE) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name == character_name]
    except OSError:
        raise OSError(f"{PATH_TO_HUMANOID_BLENDER_FILE} not present.")

    if data_to.objects:
        if len(data_to.objects) > 1:
            raise ValueError(f"More than one character with name: {character_name} found.")
        else:
            return data_to.objects[0]
