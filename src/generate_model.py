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

from configuration import BASE_MODEL_IDENTIFIER, BASE_MODEL_NAME, RIGGING_TYPE, BLENDER_RENDER_ENGINE, ADD_LIGHTING
from humanoid.humanoid import Humanoid
from humanoid.humanoid_utils import set_character_id
from morphing.character_morphing import CharacterMorphing
from utilities.blender_censor_utils import remove_humanoid_censors
from utilities.blender_light_utils import add_character_lighting
from utilities.blender_utils import create_new_blender_file, set_render_engine, save_as_blender_main
from utilities.logging_factory import setup_logger

humanoid_instances = {}

log = setup_logger(__name__)


def create_new_humanoid(file_path):
    my_humanoid = _create_humanoid_base_model(file_path=file_path)

    character_morphing = CharacterMorphing(humanoid_instance=my_humanoid)
    character_morphing.change_and_apply_single_morph(morph_name="Feet_SizeZ_max", new_value=3.5)

    _finalize_humanoid_creation(humanoid=my_humanoid, file_path=file_path)


def _create_humanoid_base_model(file_path):
    create_new_blender_file(file_path)

    humanoid = Humanoid("123", "Anna-Maria",
                        BASE_MODEL_NAME, BASE_MODEL_IDENTIFIER, RIGGING_TYPE)

    blend_file_character = humanoid.copy_base_model_to_current_blender_context()

    if blend_file_character:
        set_character_id(blend_file_character)
        humanoid_instances[humanoid.base_model_identifier] = humanoid
    else:
        raise ValueError("Character base model was not found in humanoid.blend file")
    return humanoid


def _apply_configurations():
    set_render_engine(BLENDER_RENDER_ENGINE)
    if ADD_LIGHTING:
        add_character_lighting()


def _finalize_humanoid_creation(humanoid, file_path):
    remove_humanoid_censors(humanoid.name, humanoid.is_anime_model)
    save_as_blender_main(file_path)
