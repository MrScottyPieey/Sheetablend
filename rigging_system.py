import bpy
from mathutils import Matrix, Vector
import numpy as np

class Bone2D:
    """Represents a single 2D bone in the rigging system"""
    
    def __init__(self, name, x=0, y=0, length=1.0, parent=None):
        self.name = name
        self.x = x
        self.y = y
        self.length = length
        self.rotation = 0
        self.parent = parent
        self.children = []
        self.influence = 1.0
        self.is_ik = False
        self.ik_target = Vector((0, 0))
    
    def get_end_position(self):
        """Get the end position of this bone"""
        import math
        end_x = self.x + self.length * math.cos(math.radians(self.rotation))
        end_y = self.y + self.length * math.sin(math.radians(self.rotation))
        return Vector((end_x, end_y))
    
    def get_transform_matrix(self):
        """Get the local transformation matrix for this bone"""
        import math
        cos_rot = math.cos(math.radians(self.rotation))
        sin_rot = math.sin(math.radians(self.rotation))
        
        matrix = Matrix.Identity(4)
        matrix[0][0] = cos_rot
        matrix[0][1] = -sin_rot
        matrix[1][0] = sin_rot
        matrix[1][1] = cos_rot
        matrix[0][3] = self.x
        matrix[1][3] = self.y
        
        return matrix

class Skeleton2D:
    """Manages a 2D skeleton with multiple bones"""
    
    def __init__(self):
        self.bones = {}
        self.root_bones = []
        self.weights = {}  # vertex_index -> [(bone_name, weight), ...]
    
    def add_bone(self, bone):
        """Add a bone to the skeleton"""
        self.bones[bone.name] = bone
        if bone.parent is None:
            self.root_bones.append(bone)
    
    def get_bone(self, name):
        """Get a bone by name"""
        return self.bones.get(name)
    
    def set_bone_rotation(self, bone_name, rotation):
        """Set the rotation of a bone"""
        bone = self.get_bone(bone_name)
        if bone:
            bone.rotation = rotation
    
    def paint_weights(self, vertex_indices, bone_name, weight):
        """Paint weights for a bone on vertices"""
        for vertex_index in vertex_indices:
            if vertex_index not in self.weights:
                self.weights[vertex_index] = []
            
            # Check if bone already has weight for this vertex
            found = False
            for i, (name, w) in enumerate(self.weights[vertex_index]):
                if name == bone_name:
                    self.weights[vertex_index][i] = (name, weight)
                    found = True
                    break
            
            if not found:
                self.weights[vertex_index].append((bone_name, weight))
            
            # Normalize weights
            total = sum(w for _, w in self.weights[vertex_index])
            if total > 0:
                self.weights[vertex_index] = [(n, w/total) for n, w in self.weights[vertex_index]]
    
    def deform_mesh(self, mesh_obj):
        """Deform mesh based on bone positions and weights"""
        if mesh_obj.type != 'MESH':
            return
        
        mesh = mesh_obj.data
        original_positions = [(v.co.x, v.co.y, v.co.z) for v in mesh.vertices]
        
        for vertex_idx, vertex in enumerate(mesh.vertices):
            if vertex_idx not in self.weights:
                continue
            
            # Calculate weighted deformation
            new_pos = Vector((0, 0, 0))
            for bone_name, weight in self.weights[vertex_idx]:
                bone = self.get_bone(bone_name)
                if bone:
                    # Apply bone transformation to vertex
                    transform = bone.get_transform_matrix()
                    original = Vector(original_positions[vertex_idx])
                    transformed = transform @ original
                    new_pos += transformed * weight
            
            vertex.co = new_pos
        
        mesh.update()

class IKSolver:
    """Inverse Kinematics solver for 2D bones"""
    
    @staticmethod
    def solve_2d_ik(bone, target, iterations=5, tolerance=0.001):
        """Solve IK for a 2D bone chain"""
        import math
        
        for _ in range(iterations):
            end_pos = bone.get_end_position()
            distance = (target - end_pos).length
            
            if distance < tolerance:
                break
            
            # Calculate required rotation
            current_dir = Vector((math.cos(math.radians(bone.rotation)), 
                                math.sin(math.radians(bone.rotation))))
            target_dir = (target - Vector((bone.x, bone.y))).normalized()
            
            # Calculate angle between vectors
            angle = math.degrees(math.atan2(target_dir.y, target_dir.x) - 
                               math.atan2(current_dir.y, current_dir.x))
            bone.rotation += angle * 0.5

class RiggingSystem:
    """Main rigging system for sprites"""
    
    def __init__(self, context):
        self.context = context
        self.skeleton = Skeleton2D()
        self.mesh_obj = None
    
    def create_bone(self, name, x, y, length, parent_name=None):
        """Create a new bone"""
        parent_bone = self.skeleton.get_bone(parent_name) if parent_name else None
        bone = Bone2D(name, x, y, length, parent_bone)
        self.skeleton.add_bone(bone)
        
        # Add to Blender properties
        sprite_props = self.context.scene.sheetablend_props
        if not sprite_props.has_rig:
            sprite_props.has_rig = True
        
        return bone
    
    def setup_rigging_for_object(self, mesh_obj):
        """Setup rigging system for a mesh object"""
        self.mesh_obj = mesh_obj
        
        # Initialize weight painting data
        if mesh_obj.type == 'MESH':
            for vertex in mesh_obj.data.vertices:
                self.skeleton.weights[vertex.index] = []
    
    def paint_bone_weights(self, bone_name, vertices, weight):
        """Paint weights for bone on specific vertices"""
        vertex_indices = [v.index for v in vertices]
        self.skeleton.paint_weights(vertex_indices, bone_name, weight)
    
    def apply_deformation(self):
        """Apply bone deformation to the mesh"""
        if self.mesh_obj:
            self.skeleton.deform_mesh(self.mesh_obj)
    
    def set_bone_rotation(self, bone_name, rotation):
        """Set bone rotation and update mesh"""
        self.skeleton.set_bone_rotation(bone_name, rotation)
        self.apply_deformation()
    
    def apply_ik(self, bone_name, target_x, target_y):
        """Apply IK solver to a bone"""
        bone = self.skeleton.get_bone(bone_name)
        if bone:
            target = Vector((target_x, target_y))
            IKSolver.solve_2d_ik(bone, target)
            self.apply_deformation()