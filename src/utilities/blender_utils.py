import bpy


def create_new_blender_file(file_path: str, empty=True):
    bpy.ops.wm.read_factory_settings(use_empty=empty)
    save_as_blender_main(file_path)


def save_as_blender_main(file_path):
    bpy.ops.wm.save_as_mainfile(filepath=file_path)


def set_render_engine(scn, engine_name: str):
    scn.render.engine = engine_name
