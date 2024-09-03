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

import os

import bpy

from configuration import ROOT_DIR
from enums.humanoid_base_model_identifier import HumanoidBaseModelIdentifier
from enums.humanoid_base_model_names import HumanoidBaseModelName
from enums.rigging_types import RiggingType
from utilities.assets_utils import import_character_from_humanoid_blender_file


class Humanoid:
    """
    This class describes a humanoid blender model,
    *id is a unique uuid4 identifier which is used in the database,
    *name is a human-readable name, which can be duplicated,
    *base_model_name is the base model from the humanoid.blend file which should be used,
    *base_model_identifier is the phenotype for this model,
    *rigging_type is a RiggingType enum for the skeleton
    """

    def __init__(self, identifier, name, base_model_name, base_model_identifier, rigging_type):
        # TODO: set up uuid4 on creation
        self.identifier = identifier
        # TODO: which characters are allowed in a blender object name?
        self.name = name
        self.base_model_name: HumanoidBaseModelName = base_model_name
        self.base_model_identifier: HumanoidBaseModelIdentifier = base_model_identifier
        self.rigging_type: RiggingType = rigging_type
        self.morph_file_path = self.get_morph_file_path()
        self.is_anime_model = self.is_anime_model()

    def copy_base_model_to_current_blender_context(self):
        return import_character_from_humanoid_blender_file(
            self.base_model_name, self.name)

    def get_humanoid_object(self):
        """Retrieve humanoid object by name."""
        object_name = self.name
        if object_name in bpy.data.objects:
            return bpy.data.objects[object_name]
        else:
            raise ValueError(f"Object: {object_name} was not found in Blender.")

    def is_anime_model(self):
        if (self.base_model_name == HumanoidBaseModelName.ANIME_ANDROID.value
                or self.base_model_name == HumanoidBaseModelName.ANIME_GYNOID.value):
            return True
        else:
            return False

    def get_morph_file_path(self):
        path_name = self.base_model_name[len("MBLab_"):]
        return os.path.join(ROOT_DIR, f"assets/character_morphing/presets/{path_name}_morphs.json")
