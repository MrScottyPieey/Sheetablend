bl_info = {
    "name": "Sheetablend",
    "description": "2D sprite sheet importer with animation, frame-by-frame control, and 2D rigging",
    "author": "MrScottyPieey",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Image Editor, Properties",
    "warning": "",
    "wiki_url": "https://github.com/MrScottyPieey/Sheetablend",
    "tracker_url": "https://github.com/MrScottyPieey/Sheetablend/issues",
    "support": "COMMUNITY",
    "category": "Import-Export"
}

import bpy
from . import operators
from . import ui
from . import properties
from . import sprite_importer
from . import animation_player
from . import rigging_system

classes = [
    properties.SheetablendFrameProperties,
    properties.SheetablendAnimationProperties,
    properties.SheetablendBoneProperties,
    properties.SheetablendRigProperties,
    properties.SheetablendSpriteProperties,
    operators.SHEETABLEND_OT_import_sprite_sheet,
    operators.SHEETABLEND_OT_create_animation,
    operators.SHEETABLEND_OT_add_frame,
    operators.SHEETABLEND_OT_remove_frame,
    operators.SHEETABLEND_OT_create_rig,
    operators.SHEETABLEND_OT_add_bone,
    operators.SHEETABLEND_OT_paint_weights,
    operators.SHEETABLEND_OT_play_animation,
    operators.SHEETABLEND_OT_stop_animation,
    ui.SHEETABLEND_PT_sprite_import,
    ui.SHEETABLEND_PT_animation_editor,
    ui.SHEETABLEND_PT_frame_editor,
    ui.SHEETABLEND_PT_rigging_tools,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sheetablend_props = bpy.props.PointerProperty(type=properties.SheetablendSpriteProperties)
    bpy.app.handlers.frame_change_post.append(animation_player.frame_change_handler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sheetablend_props
    bpy.app.handlers.frame_change_post.remove(animation_player.frame_change_handler)

if __name__ == "__main__":
    register()