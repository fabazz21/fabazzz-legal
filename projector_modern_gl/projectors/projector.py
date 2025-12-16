"""
Projector Class
Professional projector instance with full configuration
"""

import numpy as np
from pyrr import Matrix44, Vector3, Quaternion
from .projector_database import get_projector_by_id
from .lens_database import get_lens_by_id, throw_to_fov


class Projector:
    """Professional Projector Instance"""

    # Class-level ID counter
    _id_counter = 0

    def __init__(self, model_id, lens_id, ctx, position=(0, 2.5, 10)):
        """Initialize projector"""
        # Generate unique ID
        Projector._id_counter += 1
        self.id = Projector._id_counter

        # Get configuration from database
        self.config = get_projector_by_id(model_id)
        if not self.config:
            raise ValueError(f"Unknown projector model: {model_id}")

        self.model_id = model_id
        self.name = f"{self.config['name']} #{self.id}"

        # Lens configuration
        self.lens_id = lens_id
        self.lens_config = get_lens_by_id(lens_id)
        if not self.lens_config:
            raise ValueError(f"Unknown lens: {lens_id}")

        self.throw_ratio = self.lens_config['throw_min']

        # ModernGL context
        self.ctx = ctx

        # Transform
        self.position = Vector3(position)
        self.rotation = Quaternion()
        self.target_position = self.position + Vector3([0, 0, -8])

        # Camera parameters
        self.near = 0.1
        self.far = 200.0
        self.projection_far = 500.0
        self.aspect = self.config['aspect']

        # Lens shift (fraction of frame, -1 to 1)
        self.lens_shift_h = 0.0  # Horizontal shift
        self.lens_shift_v = 0.0  # Vertical shift

        # Keystone correction
        self.keystone_v = 0.0  # Vertical (-50 to +50)
        self.keystone_h = 0.0  # Horizontal (-50 to +50)

        # Keystone corners (independent X/Y control, -100 to +100)
        self.keystone_tl_x = 0.0
        self.keystone_tl_y = 0.0
        self.keystone_tr_x = 0.0
        self.keystone_tr_y = 0.0
        self.keystone_bl_x = 0.0
        self.keystone_bl_y = 0.0
        self.keystone_br_x = 0.0
        self.keystone_br_y = 0.0

        # Corner pin (independent corner control, -100 to +100)
        self.corner_pin_tl_x = 0.0
        self.corner_pin_tl_y = 0.0
        self.corner_pin_tr_x = 0.0
        self.corner_pin_tr_y = 0.0
        self.corner_pin_bl_x = 0.0
        self.corner_pin_bl_y = 0.0
        self.corner_pin_br_x = 0.0
        self.corner_pin_br_y = 0.0

        # Soft edge blending
        self.soft_edge_l = 0.0  # Left (0-100%)
        self.soft_edge_r = 0.0  # Right (0-100%)
        self.soft_edge_t = 0.0  # Top (0-100%)
        self.soft_edge_b = 0.0  # Bottom (0-100%)
        self.soft_edge_gamma = 2.2  # Gamma curve (0.1-10.0)

        # Projection settings
        self.intensity = 1.0
        self.active = True

        # Shadow mapping
        self.shadow_bias = 0.003
        self.depth_fbo_index = None  # Will be assigned by renderer

        # Texture
        self.texture = None

        # Frustum visualization
        self.frustum_lines = None

        # Orientation
        self.orientation = 'landscape'  # or 'portrait'

        print(f"  ✅ Created {self.name} with {self.lens_config['name']}")

    def get_fov(self):
        """Get current field of view based on throw ratio"""
        return throw_to_fov(self.throw_ratio, self.aspect)

    def get_view_matrix(self):
        """Get view matrix (from projector's perspective)"""
        # Look from position towards target
        forward = self.target_position - self.position
        if np.linalg.norm(forward) > 0:
            forward = forward / np.linalg.norm(forward)

        # Up vector
        up = Vector3([0, 1, 0])

        # Right vector
        right = np.cross(forward, up)
        if np.linalg.norm(right) > 0:
            right = right / np.linalg.norm(right)

        # Recalculate up
        up = np.cross(right, forward)

        # Build view matrix
        view = Matrix44.look_at(
            self.position,
            self.target_position,
            up
        )

        return np.array(view, dtype=np.float32)

    def get_projection_matrix(self):
        """Get projection matrix with optional lens shift"""
        fov = self.get_fov()
        projection = Matrix44.perspective_projection(
            fov,
            self.aspect,
            self.near,
            self.far
        )

        # Apply lens shift via off-axis projection
        if self.lens_shift_h != 0.0 or self.lens_shift_v != 0.0:
            # Modify projection matrix elements [8] and [9]
            proj_array = np.array(projection, dtype=np.float32)
            proj_array[2, 0] = 2.0 * self.lens_shift_h  # Horizontal shift
            proj_array[2, 1] = 2.0 * self.lens_shift_v  # Vertical shift
            return proj_array

        return np.array(projection, dtype=np.float32)

    def get_shadow_matrix(self):
        """Get combined shadow matrix (projection * view)"""
        return self.get_projection_matrix() @ self.get_view_matrix()

    def get_model_matrix(self):
        """Get model matrix (identity for projector itself)"""
        # Projectors don't have a model matrix (they're in world space)
        return np.eye(4, dtype=np.float32)

    def set_throw_ratio(self, ratio):
        """Set throw ratio within lens limits"""
        min_throw = self.lens_config['throw_min']
        max_throw = self.lens_config['throw_max']
        self.throw_ratio = np.clip(ratio, min_throw, max_throw)

    def set_lens_shift(self, h, v):
        """Set lens shift (normalized -1 to 1)"""
        max_h = self.lens_config['shift_h'] / 100.0
        max_v = self.lens_config['shift_v'] / 100.0

        self.lens_shift_h = np.clip(h, -max_h, max_h)
        self.lens_shift_v = np.clip(v, -max_v, max_v)

    def set_keystone(self, v, h):
        """Set keystone correction"""
        self.keystone_v = np.clip(v, -50.0, 50.0)
        self.keystone_h = np.clip(h, -50.0, 50.0)

    def reset_keystone(self):
        """Reset all keystone parameters to zero"""
        self.keystone_v = 0.0
        self.keystone_h = 0.0
        self.keystone_tl_x = 0.0
        self.keystone_tl_y = 0.0
        self.keystone_tr_x = 0.0
        self.keystone_tr_y = 0.0
        self.keystone_bl_x = 0.0
        self.keystone_bl_y = 0.0
        self.keystone_br_x = 0.0
        self.keystone_br_y = 0.0

    def reset_corner_pin(self):
        """Reset all corner pin parameters to zero"""
        self.corner_pin_tl_x = 0.0
        self.corner_pin_tl_y = 0.0
        self.corner_pin_tr_x = 0.0
        self.corner_pin_tr_y = 0.0
        self.corner_pin_bl_x = 0.0
        self.corner_pin_bl_y = 0.0
        self.corner_pin_br_x = 0.0
        self.corner_pin_br_y = 0.0

    def reset_soft_edge(self):
        """Reset all soft edge parameters"""
        self.soft_edge_l = 0.0
        self.soft_edge_r = 0.0
        self.soft_edge_t = 0.0
        self.soft_edge_b = 0.0
        self.soft_edge_gamma = 2.2

    def set_texture(self, texture):
        """Set projection texture"""
        self.texture = texture

    def load_texture_from_file(self, filepath):
        """Load texture from image file"""
        from PIL import Image

        img = Image.open(filepath).convert('RGB')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL expects bottom-left origin

        self.texture = self.ctx.texture(img.size, 3, img.tobytes())
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.texture.repeat_x = False
        self.texture.repeat_y = False

        print(f"  ✅ Loaded texture: {filepath} ({img.size[0]}x{img.size[1]})")

    def create_test_pattern(self, width=1920, height=1080):
        """Create test pattern texture"""
        from PIL import Image, ImageDraw

        # Create test pattern
        img = Image.new('RGB', (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw grid
        grid_size = 120
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255), width=2)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255), width=2)

        # Draw center cross
        draw.line([(width//2, 0), (width//2, height)], fill=(255, 0, 0), width=4)
        draw.line([(0, height//2), (width, height//2)], fill=(255, 0, 0), width=4)

        # Corner markers
        marker_size = 60
        draw.rectangle([0, 0, marker_size, marker_size], fill=(0, 255, 0))
        draw.rectangle([width-marker_size, 0, width, marker_size], fill=(0, 255, 0))
        draw.rectangle([0, height-marker_size, marker_size, height], fill=(0, 255, 0))
        draw.rectangle([width-marker_size, height-marker_size, width, height], fill=(0, 255, 0))

        # Center circle
        draw.ellipse([width//2-100, height//2-100, width//2+100, height//2+100],
                    outline=(0, 255, 255), width=4)

        # Convert to texture
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.texture = self.ctx.texture(img.size, 3, img.tobytes())
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

        print(f"  ✅ Created test pattern ({width}x{height})")

    def update(self, dt):
        """Update projector (called every frame)"""
        # Update frustum visualization if needed
        pass

    def cleanup(self):
        """Cleanup resources"""
        if self.texture:
            self.texture.release()

    def __repr__(self):
        return f"<Projector {self.name} at ({self.position[0]:.1f}, {self.position[1]:.1f}, {self.position[2]:.1f})>"
