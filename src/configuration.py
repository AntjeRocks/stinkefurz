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

import os

from enums.blender_render_engines import BlenderRenderEngine
from enums.humanoid_base_model_identifier import HumanoidBaseModelIdentifier
from enums.humanoid_base_model_names import HumanoidBaseModelName
from enums.rigging_types import RiggingType

# set up the project root dir in (/src)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# which character set up to use TODO: delete me
BASE_MODEL_IDENTIFIER: str = HumanoidBaseModelIdentifier.CAUCASIAN_GYNOID.value
RIGGING_TYPE: str = RiggingType.BASE_INVERSE_KINEMATICS.value
BASE_MODEL_NAME: str = HumanoidBaseModelName.GYNOID.value

# basic config
ADD_LIGHTING = True
BLENDER_RENDER_ENGINE = BlenderRenderEngine.BLENDER_EEVEE
