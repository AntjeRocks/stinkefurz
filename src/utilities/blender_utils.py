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

from enums.blender_render_engines import (BlenderRenderEngine)
from utilities import blender_const
from utilities.logging_factory import setup_logger

log = setup_logger(__name__)


def create_new_blender_file(file_path: str, empty=True):
    """
    Create a new Blender File, overwrites file if it's present
    rename the main scene to MAIN_SCENE_NAME,
    and save it
    """
    log.info(f"Creating new Blender File in: {file_path}")
    bpy.ops.wm.read_factory_settings(use_empty=empty)
    rename_scene(bpy.context.scene, blender_const.MAIN_SCENE_NAME)
    save_as_blender_main(file_path)


def save_as_blender_main(file_path: str):
    """Save a Blender File as main with given file_path, overwrites file if it's present"""
    log.info(f"Saving Blender File in: {file_path}")
    bpy.ops.wm.save_as_mainfile(filepath=file_path)


def rename_scene(scene: bpy.types.Scene, new_scene_name: str):
    """"Rename a given scene to new_scene_name"""
    log.info(f"Renaming Main Scene to: {new_scene_name}")
    scene.name = new_scene_name
    bpy.context.window.scene = scene


def get_scene(scene_name: str = blender_const.MAIN_SCENE_NAME):
    """"
    Returns main scene,
    when scene_name is defined it will return given scene with scene_name,
    it will create the given scene_name if it doesn't exist and return it
    """
    scene = bpy.data.scenes.get(scene_name)
    bpy.context.window.scene = bpy.data.scenes[scene_name]
    if scene is not None:
        return scene
    else:
        new_scene = bpy.data.scenes.new(name=scene_name)
        return new_scene


def set_render_engine(engine: BlenderRenderEngine):
    """Set render engine to given engine Enum"""
    log.info(f"Setting up Blender Render Engine to: {engine.value}")
    bpy.context.scene.render.engine = engine.value


def get_or_create_collection(collection_name: str, parent_collection=None):
    """"
    Getting collection by name,
    adding a new collection if it doesn't exist,
    if parent_collection is empty it will be saved in root,
    if parent_collection given it will be linked as child of this parent
    """
    if parent_collection is None:
        parent_collection = bpy.context.scene.collection

    if not parent_collection:
        raise ValueError("add_new_collection: Parent collection is invalid. Ensure it is correctly set.")

    existing_collection = parent_collection.children.get(collection_name)

    if existing_collection is None:
        log.info(f"Creating new collection: {collection_name} as child of: {parent_collection.name}")
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection)
        return new_collection
    else:
        log.info(f"Collection: {collection_name} already exists")
        return existing_collection
