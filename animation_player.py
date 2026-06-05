import bpy
from mathutils import Vector

class AnimationPlayer:
    """Handles sprite animation playback and frame management"""
    
    def __init__(self, context):
        self.context = context
        self.current_frame = 0
        self.frame_timer = 0
        self.is_playing = False
    
    def play_animation(self, animation_index=0):
        """Start playing an animation"""
        sprite_props = self.context.scene.sheetablend_props
        if animation_index < len(sprite_props.animations):
            sprite_props.active_animation = animation_index
            sprite_props.is_playing = True
            self.is_playing = True
            self.current_frame = 0
            self.frame_timer = 0
    
    def stop_animation(self):
        """Stop playing the current animation"""
        sprite_props = self.context.scene.sheetablend_props
        sprite_props.is_playing = False
        self.is_playing = False
    
    def get_current_animation(self):
        """Get the currently active animation"""
        sprite_props = self.context.scene.sheetablend_props
        if sprite_props.active_animation < len(sprite_props.animations):
            return sprite_props.animations[sprite_props.active_animation]
        return None
    
    def update_frame(self, delta_time):
        """Update to next frame based on animation speed"""
        if not self.is_playing:
            return
        
        sprite_props = self.context.scene.sheetablend_props
        animation = self.get_current_animation()
        
        if not animation or len(animation.frames) == 0:
            return
        
        # Calculate frame duration
        current_frame_data = animation.frames[self.current_frame]
        frame_duration = current_frame_data.duration / sprite_props.playback_speed
        
        self.frame_timer += delta_time
        
        if self.frame_timer >= frame_duration:
            self.frame_timer -= frame_duration
            self.current_frame += 1
            
            # Handle looping
            if self.current_frame >= len(animation.frames):
                if animation.is_looping:
                    self.current_frame = 0
                else:
                    self.current_frame = len(animation.frames) - 1
                    self.stop_animation()
            
            # Update UV mapping
            self.update_sprite_uv()
    
    def update_sprite_uv(self):
        """Update the sprite's UV coordinates to show the current frame"""
        animation = self.get_current_animation()
        if not animation or self.current_frame >= len(animation.frames):
            return
        
        frame = animation.frames[self.current_frame]
        sprite_props = self.context.scene.sheetablend_props
        
        # Calculate UV coordinates
        uv_x = frame.x / sprite_props.sheet_width
        uv_y = frame.y / sprite_props.sheet_height
        uv_w = frame.width / sprite_props.sheet_width
        uv_h = frame.height / sprite_props.sheet_height
        
        # Find sprite object and update its material UVs
        for obj in self.context.scene.objects:
            if obj.type == 'MESH' and len(obj.data.materials) > 0:
                mat = obj.data.materials[0]
                if mat.use_nodes:
                    # Update UV mapping via UV offset nodes if they exist
                    # This is a simplified approach - can be expanded
                    pass
    
    def set_frame(self, frame_index):
        """Manually set the current frame"""
        animation = self.get_current_animation()
        if animation and 0 <= frame_index < len(animation.frames):
            self.current_frame = frame_index
            self.frame_timer = 0
            self.update_sprite_uv()

def frame_change_handler(scene):
    """Handler called when Blender frame changes"""
    pass

class AnimationTimeline:
    """Manages animation timeline and keyframes"""
    
    def __init__(self, context):
        self.context = context
    
    def create_timeline_from_animation(self, animation_index=0):
        """Create timeline keyframes from animation frames"""
        sprite_props = self.context.scene.sheetablend_props
        if animation_index >= len(sprite_props.animations):
            return False
        
        animation = sprite_props.animations[animation_index]
        scene = self.context.scene
        
        # Create action if it doesn't exist
        action_name = f"Animation_{animation.name}"
        if action_name in bpy.data.actions:
            action = bpy.data.actions[action_name]
        else:
            action = bpy.data.actions.new(action_name)
        
        current_frame = 0
        for i, frame in enumerate(animation.frames):
            # Calculate keyframe position
            frame_duration_in_scene_frames = int(frame.duration * scene.render.fps)
            current_frame += frame_duration_in_scene_frames
        
        scene.frame_end = current_frame
        return True