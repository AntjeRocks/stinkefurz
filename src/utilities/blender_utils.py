# Stinkefurz
#
# Stinkefurz fork website : https://github.com/AntjeRocks/stinkefurz
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

import bpy

from enums.blender_render_engines import (BlenderRenderEngine)
from enums.blender_scene_names import BlenderSceneNames
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def create_new_blender_file(file_path: str, empty=True):
    log.info(f"Creating new Blender File in: {file_path}")
    bpy.ops.wm.read_factory_settings(use_empty=empty)
    rename_scene_main(bpy.context.scene)
    save_as_blender_main(file_path)


def save_as_blender_main(file_path):
    log.info(f"Saving Blender File in: {file_path}")
    bpy.ops.wm.save_as_mainfile(filepath=file_path)


def rename_scene_main(scn):
    scene_name = BlenderSceneNames.MAIN_SCENE.value
    log.info(f"Renaming Main Scene to: {scene_name}")
    scn.name = scene_name


def set_render_engine(engine: BlenderRenderEngine):
    log.info(f"Setting up Blender Render Engine to: {engine.value}")
    bpy.context.scene.render.engine = engine.value
