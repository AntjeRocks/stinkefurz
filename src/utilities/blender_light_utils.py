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

from math import radians

import bpy

from utilities import blender_const
from utilities.blender_utils import get_or_create_collection
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def add_character_lighting():
    """Adds 3 area lights"""
    log.info(f"Create studio lights")
    _create_area_light(name="light_key",
                       location=(1.5, -1.5, 2.5),
                       rotation=(0, -70, 133),
                       color=(0.688, 0.914, 1),
                       )
    _create_area_light(name="light_backlight",
                       energy=150,
                       location=(-1.5, 1.5, 2.5),
                       rotation=(-60, 0, 40),
                       color=(1, 1, 1),
                       )
    _create_area_light(name="light_fill",
                       location=(-1.5, -2, 2.5),
                       rotation=(0, -70, 50),
                       color=(0.981, 1, 0.694),
                       )


def _create_area_light(name, energy=100.0, location=(0, 0, 5), rotation=(0.0, 0.0, 0.0),
                       color=(1, 1, 1), shadows_enabled=True, use_contact_shadow=True):
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = energy
    light_data.color = color
    light_data.use_shadow = shadows_enabled
    light_data.use_contact_shadow = use_contact_shadow
    light_object = bpy.data.objects.new(name=name, object_data=light_data)
    light_object.location = location
    light_object.rotation_euler = (radians(rotation[0]), radians(rotation[1]), radians(rotation[2]))
    light_collection = get_or_create_collection(blender_const.LIGHT_COLLECTION_NAME)
    light_collection.objects.link(light_object)
