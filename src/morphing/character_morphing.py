# # Stinkefurz
# #
# # Stinkefurz fork website : https://github.com/AntjeRocks/stinkefurz
# #
# # Portions of this code are derived from the MB-Lab project:
# # https://github.com/animate1978/MB-Lab
# #
# # ##### BEGIN GPL LICENSE BLOCK #####
# #
# #  This program is free software; you can redistribute it and/or
# #  modify it under the terms of the GNU General Public License
# #  as published by the Free Software Foundation; either version 3
# #  of the License, or (at your option) any later version.
# #
# #  This program is distributed in the hope that it will be useful,
# #  but WITHOUT ANY WARRANTY; without even the implied warranty of
# #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #  GNU General Public License for more details.
# #
# #  You should have received a copy of the GNU General Public License
# #  along with this program; if not, write to the Free Software Foundation,
# #  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# #
# # ##### END GPL LICENSE BLOCK #####
# #
# # ManuelbastioniLAB - Copyright (C) 2015-2018 Manuel Bastioni

# mathutils are imported via blender runnable
# noinspection PyUnresolvedReferences
import mathutils

from utilities.file_utils import load_json_file
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


class CharacterMorphing:
    def __init__(self, humanoid_instance):
        self.humanoid_instance = humanoid_instance
        self.morph_data = self._load_morph_data()
        self.final_form = self._load_vertices()

    def _load_vertices(self):
        """Load the vertices from the object into the final_form list."""
        obj = self.humanoid_instance.get_humanoid_object()
        return [vert.co.copy() for vert in obj.data.vertices]

    def _load_morph_data(self):
        """Load morph data from JSON file."""
        return load_json_file(self.humanoid_instance.morph_file_path)

    def change_and_apply_single_morph(self, morph_name, new_value):
        """Modify the object based on a single morph name and new value."""
        if morph_name in self.morph_data:
            morph_deltas = self.morph_data[morph_name]
            for d_data in morph_deltas:
                vertex_index = d_data[0]
                delta = mathutils.Vector(d_data[1:]) * new_value
                self.final_form[vertex_index] += delta
            self.apply_morph_changes_to_final_form()
        else:
            log.error(f"Morph: {morph_name} was not found in the morph_data")

    def apply_morph_changes_to_final_form(self):
        """Update the object's vertices in Blender based on final_form."""
        obj = self.humanoid_instance.get_humanoid_object()
        for i, vert in enumerate(obj.data.vertices):
            vert.co = self.final_form[i]
