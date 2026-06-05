import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty, FloatProperty
from . import sprite_importer, animation_player, rigging_system

class SHEETABLEND_OT_import_sprite_sheet(Operator):
    """Import a sprite sheet and create frames"""
    bl_idname = "sheetablend.import_sprite_sheet"
    bl_label = "Import Sprite Sheet"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}
        
        sprite_props = context.scene.sheetablend_props
        
        result = sprite_importer.import_sprite_sheet(
            context,
            self.filepath,
            sprite_props.grid_cols,
            sprite_props.grid_rows,
            sprite_props.spacing_x,
            sprite_props.spacing_y
        )
        
        if result:
            self.report({'INFO'}, f"Imported sprite sheet with {len(sprite_props.animations[0].frames)} frames")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to import sprite sheet")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SHEETABLEND_OT_create_animation(Operator):
    """Create a new animation"""
    bl_idname = "sheetablend.create_animation"
    bl_label = "Create Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    anim_name: StringProperty(name="Animation Name", default="New Animation")
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        
        animation = sprite_props.animations.add()
        animation.name = self.anim_name
        
        self.report({'INFO'}, f"Created animation '{self.anim_name}'")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SHEETABLEND_OT_add_frame(Operator):
    """Add a frame to the current animation"""
    bl_idname = "sheetablend.add_frame"
    bl_label = "Add Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        if sprite_props.active_animation >= len(sprite_props.animations):
            self.report({'ERROR'}, "No active animation")
            return {'CANCELLED'}
        
        animation = sprite_props.animations[sprite_props.active_animation]
        frame = animation.frames.add()
        frame.name = f"Frame_{len(animation.frames)}"
        
        self.report({'INFO'}, "Frame added")
        return {'FINISHED'}

class SHEETABLEND_OT_remove_frame(Operator):
    """Remove the selected frame from current animation"""
    bl_idname = "sheetablend.remove_frame"
    bl_label = "Remove Frame"
    bl_options = {'REGISTER', 'UNDO'}
    
    frame_index: IntProperty(name="Frame Index", default=0, min=0)
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        if sprite_props.active_animation >= len(sprite_props.animations):
            self.report({'ERROR'}, "No active animation")
            return {'CANCELLED'}
        
        animation = sprite_props.animations[sprite_props.active_animation]
        if 0 <= self.frame_index < len(animation.frames):
            animation.frames.remove(self.frame_index)
            self.report({'INFO'}, "Frame removed")
            return {'FINISHED'}
        
        self.report({'ERROR'}, "Invalid frame index")
        return {'CANCELLED'}

class SHEETABLEND_OT_create_rig(Operator):
    """Create a new 2D rig for the sprite"""
    bl_idname = "sheetablend.create_rig"
    bl_label = "Create Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        
        # Create new rig
        if not sprite_props.rig:
            sprite_props.rig = context.scene.sheetablend_props.__class__.SheetablendRigProperties()
        
        sprite_props.rig.name = "Sprite Rig"
        sprite_props.has_rig = True
        
        self.report({'INFO'}, "Created new rig")
        return {'FINISHED'}

class SHEETABLEND_OT_add_bone(Operator):
    """Add a new bone to the rig"""
    bl_idname = "sheetablend.add_bone"
    bl_label = "Add Bone"
    bl_options = {'REGISTER', 'UNDO'}
    
    bone_name: StringProperty(name="Bone Name", default="Bone")
    x: FloatProperty(name="X Position", default=0.0)
    y: FloatProperty(name="Y Position", default=0.0)
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        if not sprite_props.has_rig:
            self.report({'ERROR'}, "No rig exists. Create one first.")
            return {'CANCELLED'}
        
        bone = sprite_props.rig.bones.add()
        bone.name = self.bone_name
        bone.x = self.x
        bone.y = self.y
        
        self.report({'INFO'}, f"Added bone '{self.bone_name}'")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SHEETABLEND_OT_paint_weights(Operator):
    """Paint bone weights on mesh vertices"""
    bl_idname = "sheetablend.paint_weights"
    bl_label = "Paint Weights"
    bl_options = {'REGISTER', 'UNDO'}
    
    weight: FloatProperty(name="Weight", default=1.0, min=0.0, max=1.0, subtype='FACTOR')
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        
        if not sprite_props.has_rig or sprite_props.rig.current_bone < 0:
            self.report({'ERROR'}, "No bone selected")
            return {'CANCELLED'}
        
        sprite_props.rig.weight_painting_enabled = True
        self.report({'INFO'}, "Weight painting enabled")
        return {'FINISHED'}

class SHEETABLEND_OT_play_animation(Operator):
    """Play the selected animation"""
    bl_idname = "sheetablend.play_animation"
    bl_label = "Play Animation"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        sprite_props.is_playing = True
        
        self.report({'INFO'}, "Playing animation")
        return {'FINISHED'}

class SHEETABLEND_OT_stop_animation(Operator):
    """Stop the current animation"""
    bl_idname = "sheetablend.stop_animation"
    bl_label = "Stop Animation"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        sprite_props = context.scene.sheetablend_props
        sprite_props.is_playing = False
        
        self.report({'INFO'}, "Stopped animation")
        return {'FINISHED'}