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

import os
import time

import bpy

from enums.blender_render_engines import BlenderRenderEngine
from mb_lab import algorithms, object_ops
from mb_lab import creation_tools_ops
from mb_lab import file_ops
from mb_lab import humanoid
from mb_lab import measurescreator
from mb_lab import morphcreator
from utilities import blender_utils
from utilities.logging_factory import setup_logger

add_lamps = True
mblab_humanoid = humanoid.Humanoid("1.8.1")

log = setup_logger(__name__)


def create_new_humanoid(file_path):
    log.info("MOEp")
    blender_utils.create_new_blender_file(file_path)

    file_ops.configuration_done = None
    character_identifier = "f_ca01"

    rigging_type = "base"
    lib_filepath = file_ops.get_blendlibrary_path()

    characters_config = file_ops.get_configuration()
    base_model_name = characters_config[character_identifier]["template_model"]
    obj = file_ops.import_object_from_lib(lib_filepath, base_model_name, character_identifier)
    if obj is not None:
        obj["manuellab_vers"] = "1.8.1"
        obj["manuellab_id"] = character_identifier
        obj["manuellab_rig"] = rigging_type
    mblab_humanoid.init_database(obj, character_identifier, rigging_type)
    if mblab_humanoid.has_data:
        blender_utils.set_render_engine(BlenderRenderEngine.BLENDER_EEVEE)
        if add_lamps:
            object_ops.add_lighting()

        init_morphing_props(mblab_humanoid)
        init_categories_props(mblab_humanoid)
        init_measures_props(mblab_humanoid)
        # init_restposes_props(mblab_humanoid)
        init_presets_props(mblab_humanoid)
        init_ethnic_props(mblab_humanoid)
        init_metaparameters_props(mblab_humanoid)
        init_material_parameters_props(mblab_humanoid)
        mblab_humanoid.update_materials()

        mblab_humanoid.reset_mesh()
        mblab_humanoid.update_character(mode="update_all")

        # All inits for creation tools.
        morphcreator.init_morph_names_database()
        # mbcrea_expressionscreator.reset_expressions_items()
        # mbcrea_transfor.set_scene(scn)
        init_cmd_props(mblab_humanoid)
        measurescreator.init_all()
        creation_tools_ops.init_config()
        algorithms.deselect_all_objects()
    algorithms.remove_censors()
    blender_utils.save_as_blender_main(file_path)


def init_morphing_props(humanoid_instance):
    for prop in humanoid_instance.character_data:
        setattr(
            bpy.types.Object,
            prop,
            bpy.props.FloatProperty(
                name=prop.split("_")[1],
                min=-5.0,
                max=5.0,
                soft_min=0.0,
                soft_max=1.0,
                precision=3,
                default=0.5,
                subtype='FACTOR',
                update=realtime_update))


def realtime_update(self, context):
    if mblab_humanoid.bodydata_realtime_activated:
        time1 = time.time()
        scn = bpy.context.scene
        mblab_humanoid.update_character(category_name=scn.morphingCategory, mode="update_realtime")
        if scn.morphingCategory != "Expressions":
            mblab_humanoid.update_character(category_name="Expressions", mode="update_realtime")
        mblab_humanoid.sync_gui_according_measures()
        print("realtime_update: {0}".format(time.time() - time1))


def init_categories_props(humanoid_instance):
    bpy.types.Scene.morphingCategory = bpy.props.EnumProperty(
        items=get_categories_enum(),
        update=sync_character_to_props,
        name="Morphing categories")

    # Sub-categories for "Facial expressions"
    # mbcrea_expressionscreator.set_expressions_modifiers(mblab_humanoid)
    # sub_categories_enum = mbcrea_expressionscreator.get_expressions_sub_categories()

    # bpy.types.Scene.expressionsSubCategory = bpy.props.EnumProperty(
    #     items=sub_categories_enum,
    #     update=sync_character_to_props,
    #     name="Expressions sub-categories")

    # Special properties used by transfor.Transfor
    bpy.types.Scene.transforMorphingCategory = bpy.props.EnumProperty(
        items=get_categories_enum(["Expressions"]),
        update=sync_character_to_props,
        name="Morphing categories")


def sync_character_to_props(self, context):
    mblab_humanoid.sync_character_data_to_obj_props()
    mblab_humanoid.update_character()


def get_categories_enum(exclude=None):
    if exclude is None:
        exclude = []
    categories_enum = []
    # All categories for "Body Measures"
    for category in mblab_humanoid.get_categories(exclude):
        categories_enum.append(
            (category.name, category.name, category.name))
    return categories_enum


def init_measures_props(humanoid_instance):
    for measure_name, measure_val in humanoid_instance.morph_engine.measures.items():
        setattr(
            bpy.types.Object,
            measure_name,
            bpy.props.FloatProperty(
                name=measure_name, min=0.0, max=500.0,
                subtype='FACTOR',
                default=measure_val))
    humanoid_instance.sync_gui_according_measures()


def init_restposes_props(humanoid_instance):
    if humanoid_instance.exists_rest_poses_database():
        restpose_items = file_ops.generate_items_list(humanoid_instance.restposes_path)
        bpy.types.Object.rest_pose = bpy.props.EnumProperty(
            items=restpose_items,
            name="Rest pose",
            default=restpose_items[0][0],
            update=restpose_update)


def restpose_update(self, context):
    armature = mblab_humanoid.get_armature()
    filepath = os.path.join(
        mblab_humanoid.restposes_path,
        "".join([armature.rest_pose, ".json"]))
    # mblab_retarget.load_pose(filepath, armature)


def init_presets_props(humanoid_instance):
    if humanoid_instance.exists_preset_database():
        preset_items = file_ops.generate_items_list(humanoid_instance.presets_path)
        bpy.types.Object.preset = bpy.props.EnumProperty(
            items=preset_items,
            name="Types",
            update=preset_update)


def init_ethnic_props(humanoid_instance):
    if humanoid_instance.exists_phenotype_database():
        ethnic_items = file_ops.generate_items_list(humanoid_instance.phenotypes_path)
        bpy.types.Object.ethnic = bpy.props.EnumProperty(
            items=ethnic_items,
            name="Phenotype",
            update=ethnic_update)


def init_metaparameters_props(humanoid_instance):
    for meta_data_prop in humanoid_instance.character_metaproperties.keys():
        upd_function = None

        if "age" in meta_data_prop:
            upd_function = age_update
        if "mass" in meta_data_prop:
            upd_function = mass_update
        if "tone" in meta_data_prop:
            upd_function = tone_update
        if "last" in meta_data_prop:
            upd_function = None

        if "last_" not in meta_data_prop:
            setattr(
                bpy.types.Object,
                meta_data_prop,
                bpy.props.FloatProperty(
                    name=meta_data_prop, min=-1.0, max=1.0,
                    precision=3,
                    default=0.0,
                    subtype='FACTOR',
                    update=upd_function))


def preset_update(self, context):
    scn = bpy.context.scene
    obj = mblab_humanoid.get_object()
    filepath = os.path.join(
        mblab_humanoid.presets_path,
        "".join([obj.preset, ".json"]))
    mblab_humanoid.load_character(filepath, mix=scn.mblab_mix_characters)


def ethnic_update(self, context):
    scn = bpy.context.scene
    obj = mblab_humanoid.get_object()
    filepath = os.path.join(
        mblab_humanoid.phenotypes_path,
        "".join([obj.ethnic, ".json"]))
    mblab_humanoid.load_character(filepath, mix=scn.mblab_mix_characters)


def age_update(self, context):
    time1 = time.time()
    if mblab_humanoid.metadata_realtime_activated:
        time1 = time.time()
        mblab_humanoid.calculate_transformation("AGE")


def mass_update(self, context):
    if mblab_humanoid.metadata_realtime_activated:
        mblab_humanoid.calculate_transformation("FAT")


def tone_update(self, context):
    if mblab_humanoid.metadata_realtime_activated:
        mblab_humanoid.calculate_transformation("MUSCLE")


def init_material_parameters_props(humanoid_instance):
    for material_data_prop, value in humanoid_instance.character_material_properties.items():
        setattr(
            bpy.types.Object,
            material_data_prop,
            bpy.props.FloatProperty(
                name=material_data_prop,
                min=0.0,
                max=1.0,
                precision=2,
                subtype='FACTOR',
                update=material_update,
                default=value))


def material_update(self, context):
    if mblab_humanoid.material_realtime_activated:
        mblab_humanoid.update_materials(update_textures_nodes=False)


def init_cmd_props(humanoid_instance):
    for prop in morphcreator.get_all_cmd_attr_names(humanoid_instance):
        setattr(
            bpy.types.Object,
            prop,
            bpy.props.BoolProperty(
                name=prop.split("_")[2],
                default=False))
