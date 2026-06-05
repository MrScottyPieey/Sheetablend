import bpy
from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
    IntVectorProperty,
    FloatVectorProperty
)

class SheetablendFrameProperties(bpy.types.PropertyGroup):
    """Properties for individual sprite frames"""
    name: StringProperty(name="Frame Name", default="Frame")
    x: IntProperty(name="X Position", default=0, min=0)
    y: IntProperty(name="Y Position", default=0, min=0)
    width: IntProperty(name="Width", default=64, min=1)
    height: IntProperty(name="Height", default=64, min=1)
    duration: FloatProperty(name="Duration", default=0.1, min=0.01, max=10.0)
    enabled: BoolProperty(name="Enabled", default=True)
    pivot_x: FloatProperty(name="Pivot X", default=0.5, min=0.0, max=1.0)
    pivot_y: FloatProperty(name="Pivot Y", default=0.5, min=0.0, max=1.0)

class SheetablendAnimationProperties(bpy.types.PropertyGroup):
    """Properties for sprite animations"""
    name: StringProperty(name="Animation Name", default="New Animation")
    frames: CollectionProperty(type=SheetablendFrameProperties, name="Frames")
    current_frame: IntProperty(name="Current Frame", default=0, min=0)
    start_frame: IntProperty(name="Start Frame", default=0, min=0)
    end_frame: IntProperty(name="End Frame", default=1, min=0)
    is_looping: BoolProperty(name="Loop", default=True)
    speed: FloatProperty(name="Speed", default=1.0, min=0.1, max=5.0)
    is_playing: BoolProperty(name="Playing", default=False)

class SheetablendBoneProperties(bpy.types.PropertyGroup):
    """Properties for 2D bones in the rigging system"""
    name: StringProperty(name="Bone Name", default="Bone")
    parent_name: StringProperty(name="Parent Bone", default="")
    x: FloatProperty(name="X Position", default=0.0)
    y: FloatProperty(name="Y Position", default=0.0)
    length: FloatProperty(name="Length", default=1.0, min=0.1)
    rotation: FloatProperty(name="Rotation", default=0.0)
    is_ik: BoolProperty(name="IK Enabled", default=False)
    ik_target_x: FloatProperty(name="IK Target X", default=0.0)
    ik_target_y: FloatProperty(name="IK Target Y", default=0.0)
    influence: FloatProperty(name="Influence", default=1.0, min=0.0, max=1.0, subtype='FACTOR')

class SheetablendRigProperties(bpy.types.PropertyGroup):
    """Properties for the 2D rigging system"""
    name: StringProperty(name="Rig Name", default="Sprite Rig")
    bones: CollectionProperty(type=SheetablendBoneProperties, name="Bones")
    current_bone: IntProperty(name="Current Bone", default=-1)
    deform_mesh: BoolProperty(name="Deform Mesh", default=True)
    show_bones: BoolProperty(name="Show Bones", default=True)
    bone_size: FloatProperty(name="Bone Size", default=0.1, min=0.01, max=1.0)
    weight_painting_enabled: BoolProperty(name="Weight Painting", default=False)
    selected_bone_for_painting: IntProperty(name="Selected Bone", default=0)

class SheetablendSpriteProperties(bpy.types.PropertyGroup):
    """Main properties for sprite sheet and animation management"""
    sprite_image_path: StringProperty(
        name="Sprite Sheet Path",
        description="Path to the sprite sheet image",
        subtype='FILE_PATH'
    )
    sheet_width: IntProperty(name="Sheet Width", default=512, min=1)
    sheet_height: IntProperty(name="Sheet Height", default=512, min=1)
    frame_width: IntProperty(name="Frame Width", default=64, min=1)
    frame_height: IntProperty(name="Frame Height", default=64, min=1)
    
    # Grid settings
    use_grid: BoolProperty(name="Use Grid", default=True)
    grid_cols: IntProperty(name="Grid Columns", default=8, min=1)
    grid_rows: IntProperty(name="Grid Rows", default=8, min=1)
    spacing_x: IntProperty(name="Spacing X", default=0, min=0)
    spacing_y: IntProperty(name="Spacing Y", default=0, min=0)
    
    # Animation settings
    animations: CollectionProperty(type=SheetablendAnimationProperties, name="Animations")
    active_animation: IntProperty(name="Active Animation", default=0, min=0)
    default_frame_duration: FloatProperty(name="Default Frame Duration", default=0.1, min=0.01, max=10.0)
    
    # Rigging settings
    rig: PointerProperty(type=SheetablendRigProperties, name="Rig")
    has_rig: BoolProperty(name="Has Rig", default=False)
    
    # Import settings
    import_as_plane: BoolProperty(name="Import as Plane", default=True)
    create_material: BoolProperty(name="Create Material", default=True)
    auto_uv: BoolProperty(name="Auto UV", default=True)
    
    # Playback settings
    playback_speed: FloatProperty(name="Playback Speed", default=1.0, min=0.1, max=5.0)
    is_playing: BoolProperty(name="Is Playing", default=False)