"""
ModernGL Renderer
Handles all rendering: depth pass, main scene, helpers
"""

import moderngl
import numpy as np
from pathlib import Path


class Renderer:
    """ModernGL Rendering System"""

    def __init__(self, ctx, width, height):
        """Initialize renderer"""
        self.ctx = ctx
        self.width = width
        self.height = height

        # Rendering settings
        self.background_color = [0.071, 0.078, 0.090]  # #121418
        self.shadow_map_size = 2048
        self.wireframe_mode = False
        self.show_frustums = False

        # Stats
        self.stats = {
            'draw_calls': 0,
            'triangles': 0
        }

        # Load shaders
        self.shader_dir = Path(__file__).parent.parent / "shaders"
        self._load_shaders()

        # Create render targets
        self._create_render_targets()

        # Line renderer for helpers
        self._create_line_renderer()

        print("✅ Renderer initialized")

    def _get_or_create_vao(self, obj, shader):
        """Get or create VAO for object"""
        if not hasattr(obj, 'vbo') or not hasattr(obj, 'ibo'):
            return None

        # Check if this is the depth shader or projector shader
        if shader == self.depth_shader:
            # Depth shader only needs position (skip normals with 12x = 12 bytes padding)
            if not hasattr(obj, 'vao_depth') or obj.vao_depth is None:
                obj.vao_depth = self.ctx.vertex_array(
                    shader,
                    [(obj.vbo, '3f 12x', 'in_position')],  # 3f position, skip 3f (12 bytes) normals
                    obj.ibo
                )
            return obj.vao_depth
        else:
            # Projector shader needs position + normal
            if obj.vao is None:
                obj.vao = self.ctx.vertex_array(
                    shader,
                    [(obj.vbo, '3f 3f', 'in_position', 'in_normal')],
                    obj.ibo
                )
            return obj.vao

    def _load_shaders(self):
        """Load all GLSL shaders"""
        # Depth shader
        depth_vs = (self.shader_dir / "depth_vertex.glsl").read_text()
        depth_fs = (self.shader_dir / "depth_fragment.glsl").read_text()
        self.depth_shader = self.ctx.program(
            vertex_shader=depth_vs,
            fragment_shader=depth_fs
        )

        # Projector shader
        proj_vs = (self.shader_dir / "projector_vertex.glsl").read_text()
        proj_fs = (self.shader_dir / "projector_fragment.glsl").read_text()
        self.projector_shader = self.ctx.program(
            vertex_shader=proj_vs,
            fragment_shader=proj_fs
        )

        print("  ✅ Shaders loaded successfully")

    def _create_render_targets(self):
        """Create framebuffers and textures for shadow mapping"""
        # Depth map size (for shadow mapping)
        self.depth_map_size = 2048

        # Create depth render targets (one per projector, max 4)
        self.depth_textures = []
        self.depth_framebuffers = []

        for i in range(4):
            # Depth texture (R32F for linear depth)
            depth_tex = self.ctx.texture(
                (self.depth_map_size, self.depth_map_size),
                components=1,
                dtype='f4'
            )
            depth_tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
            depth_tex.repeat_x = False
            depth_tex.repeat_y = False

            # Depth buffer
            depth_buffer = self.ctx.depth_renderbuffer(
                (self.depth_map_size, self.depth_map_size)
            )

            # Framebuffer
            fbo = self.ctx.framebuffer(
                color_attachments=[depth_tex],
                depth_attachment=depth_buffer
            )

            self.depth_textures.append(depth_tex)
            self.depth_framebuffers.append(fbo)

        print(f"  ✅ Created {len(self.depth_framebuffers)} depth render targets ({self.depth_map_size}x{self.depth_map_size})")

    def _create_line_renderer(self):
        """Create simple line renderer for helpers (grid, frustums, gizmo)"""
        # Simple line shader
        line_vs = """
        #version 330 core
        in vec3 in_position;
        in vec3 in_color;
        out vec3 v_color;
        uniform mat4 mvp;
        void main() {
            v_color = in_color;
            gl_Position = mvp * vec4(in_position, 1.0);
        }
        """
        line_fs = """
        #version 330 core
        in vec3 v_color;
        out vec4 fragColor;
        void main() {
            fragColor = vec4(v_color, 1.0);
        }
        """
        self.line_shader = self.ctx.program(vertex_shader=line_vs, fragment_shader=line_fs)

        # No persistent VBO - we'll create it dynamically for each draw call
        # This is simpler and more flexible for dynamic gizmo rendering

    def draw_line(self, start_pos, end_pos, color, width=2.0, camera=None, mvp_matrix=None):
        """
        Draw a single 3D line

        Args:
            start_pos: (x, y, z) start position
            end_pos: (x, y, z) end position
            color: (r, g, b) color (0.0 to 1.0)
            width: line width in pixels (default 2.0)
            camera: Camera object (if mvp_matrix not provided)
            mvp_matrix: Pre-computed MVP matrix (optional)
        """
        self.draw_lines([start_pos], [end_pos], [color], width, camera, mvp_matrix)

    def draw_lines(self, start_positions, end_positions, colors, width=2.0, camera=None, mvp_matrix=None):
        """
        Draw multiple 3D lines efficiently in a single draw call

        Args:
            start_positions: List of (x, y, z) start positions
            end_positions: List of (x, y, z) end positions
            colors: List of (r, g, b) colors or single color for all lines
            width: line width in pixels (default 2.0)
            camera: Camera object (if mvp_matrix not provided)
            mvp_matrix: Pre-computed MVP matrix (optional)
        """
        if len(start_positions) == 0:
            return

        # Get MVP matrix
        if mvp_matrix is None:
            if camera is None:
                raise ValueError("Must provide either camera or mvp_matrix")
            mvp_matrix = camera.get_projection_matrix() @ camera.get_view_matrix()

        # Handle single color for all lines
        if len(colors) == 1 or (isinstance(colors, tuple) and len(colors) == 3):
            colors = [colors] * len(start_positions)

        # Build vertex data: [x, y, z, r, g, b] for each vertex
        vertices = []
        for start, end, color in zip(start_positions, end_positions, colors):
            # Start vertex
            vertices.extend(start)
            vertices.extend(color)
            # End vertex
            vertices.extend(end)
            vertices.extend(color)

        # Convert to numpy array
        vertex_data = np.array(vertices, dtype='f4')

        # Create VBO
        vbo = self.ctx.buffer(vertex_data.tobytes())

        # Create VAO
        vao = self.ctx.vertex_array(
            self.line_shader,
            [(vbo, '3f 3f', 'in_position', 'in_color')]
        )

        # Set line width (often ignored by modern GPUs!)
        self.ctx.line_width = max(1.0, width)

        # Also try point size for debugging
        self.ctx.point_size = max(10.0, width * 2.0)

        print(f"[RENDERER] Drawing {len(start_positions)} lines with width={width}")
        print(f"[RENDERER] First line: {start_positions[0]} -> {end_positions[0]}, color={colors[0]}")

        # Set MVP matrix
        self.line_shader['mvp'].write(mvp_matrix.astype('f4').tobytes())

        # Render lines
        vao.render(moderngl.LINES)

        print(f"[RENDERER] ✅ Lines rendered successfully")

        # Cleanup
        vao.release()
        vbo.release()

    def render_depth_pass(self, projector, scene):
        """Render depth pass from projector's perspective for shadow mapping"""
        if not hasattr(projector, 'depth_fbo_index'):
            return

        fbo = self.depth_framebuffers[projector.depth_fbo_index]
        fbo.use()

        # Clear depth buffer
        self.ctx.clear(1.0, 1.0, 1.0)

        # Set depth shader uniforms
        self.depth_shader['cameraNear'] = projector.near
        self.depth_shader['cameraFar'] = projector.far

        # Get projector view and projection matrices
        view_matrix = projector.get_view_matrix()
        proj_matrix = projector.get_projection_matrix()

        # Render all shadow-casting objects
        for obj in scene.get_visible_objects():
            if not obj.cast_shadow:
                continue

            # Model matrix
            model_matrix = obj.get_model_matrix()

            # Set uniforms
            self.depth_shader['model'].write(model_matrix.astype('f4').tobytes())
            self.depth_shader['view'].write(view_matrix.astype('f4').tobytes())
            self.depth_shader['projection'].write(proj_matrix.astype('f4').tobytes())

            # Render object (create VAO if needed)
            vao = self._get_or_create_vao(obj, self.depth_shader)
            if vao is not None:
                vao.render(moderngl.TRIANGLES)

        # Unbind framebuffer
        self.ctx.screen.use()

    def render_scene(self, scene, camera):
        """Render main scene with multi-projector shader"""
        # Clear screen
        self.ctx.clear(0.071, 0.078, 0.090)

        # Get camera matrices
        view_matrix = camera.get_view_matrix()
        proj_matrix = camera.get_projection_matrix()

        # Calculate normal matrix (inverse transpose of model-view)
        # For now, assume identity model matrix
        normal_matrix = np.eye(3, dtype=np.float32)

        # Set shader uniforms (scene lighting)
        self.projector_shader['baseColor'] = (0.533, 0.533, 0.533)  # #888888
        self.projector_shader['dirLightDir'] = tuple(scene.directional_light_direction)
        self.projector_shader['ambientLightIntensity'] = scene.ambient_light_intensity
        self.projector_shader['directionalLightIntensity'] = scene.directional_light_intensity

        # Set projector uniforms
        for i in range(4):
            if i < len(scene.projectors):
                projector = scene.projectors[i]

                # Projector active
                self.projector_shader[f'projectorActive{i}'] = projector.active

                # Projection matrix
                proj_view_matrix = projector.get_projection_matrix() @ projector.get_view_matrix()
                self.projector_shader[f'projMatrix{i}'].write(proj_view_matrix.astype('f4').tobytes())

                # Shadow matrix
                shadow_matrix = projector.get_shadow_matrix()
                self.projector_shader[f'shadowMatrix{i}'].write(shadow_matrix.astype('f4').tobytes())

                # Projector position
                self.projector_shader[f'projPosition{i}'] = tuple(projector.position)

                # Intensity
                self.projector_shader[f'intensity{i}'] = projector.intensity

                # Has texture
                self.projector_shader[f'hasTexture{i}'] = projector.texture is not None

                # Bind texture
                if projector.texture:
                    projector.texture.use(i)
                    self.projector_shader[f'projTexture{i}'] = i

                # Bind shadow map
                if hasattr(projector, 'depth_fbo_index'):
                    depth_tex = self.depth_textures[projector.depth_fbo_index]
                    depth_tex.use(4 + i)
                    self.projector_shader[f'shadowMap{i}'] = 4 + i

                # Shadow settings
                shadow_view_matrix = projector.get_view_matrix()
                self.projector_shader[f'shadowViewMatrix{i}'].write(shadow_view_matrix.astype('f4').tobytes())
                self.projector_shader[f'shadowBias{i}'] = projector.shadow_bias
                self.projector_shader[f'depthMapFar{i}'] = projector.far
                self.projector_shader[f'projectionFar{i}'] = projector.projection_far

                # Keystone
                self.projector_shader[f'keystoneV{i}'] = projector.keystone_v
                self.projector_shader[f'keystoneH{i}'] = projector.keystone_h
                self.projector_shader[f'keystoneTLX{i}'] = projector.keystone_tl_x
                self.projector_shader[f'keystoneTLY{i}'] = projector.keystone_tl_y
                self.projector_shader[f'keystoneTRX{i}'] = projector.keystone_tr_x
                self.projector_shader[f'keystoneTRY{i}'] = projector.keystone_tr_y
                self.projector_shader[f'keystoneBLX{i}'] = projector.keystone_bl_x
                self.projector_shader[f'keystoneBLY{i}'] = projector.keystone_bl_y
                self.projector_shader[f'keystoneBRX{i}'] = projector.keystone_br_x
                self.projector_shader[f'keystoneBRY{i}'] = projector.keystone_br_y

                # Soft edge
                self.projector_shader[f'softEdgeL{i}'] = projector.soft_edge_l
                self.projector_shader[f'softEdgeR{i}'] = projector.soft_edge_r
                self.projector_shader[f'softEdgeT{i}'] = projector.soft_edge_t
                self.projector_shader[f'softEdgeB{i}'] = projector.soft_edge_b
                self.projector_shader[f'softEdgeGamma{i}'] = projector.soft_edge_gamma

                # Corner pin
                self.projector_shader[f'cornerPinTLX{i}'] = projector.corner_pin_tl_x
                self.projector_shader[f'cornerPinTLY{i}'] = projector.corner_pin_tl_y
                self.projector_shader[f'cornerPinTRX{i}'] = projector.corner_pin_tr_x
                self.projector_shader[f'cornerPinTRY{i}'] = projector.corner_pin_tr_y
                self.projector_shader[f'cornerPinBLX{i}'] = projector.corner_pin_bl_x
                self.projector_shader[f'cornerPinBLY{i}'] = projector.corner_pin_bl_y
                self.projector_shader[f'cornerPinBRX{i}'] = projector.corner_pin_br_x
                self.projector_shader[f'cornerPinBRY{i}'] = projector.corner_pin_br_y
            else:
                # Inactive projector slot
                self.projector_shader[f'projectorActive{i}'] = False

        # Render all visible objects
        for obj in scene.get_visible_objects():
            # Model matrix
            model_matrix = obj.get_model_matrix()

            # Set uniforms
            self.projector_shader['model'].write(model_matrix.astype('f4').tobytes())
            self.projector_shader['view'].write(view_matrix.astype('f4').tobytes())
            self.projector_shader['projection'].write(proj_matrix.astype('f4').tobytes())
            self.projector_shader['normalMatrix'].write(normal_matrix.astype('f4').tobytes())

            # Render object (create VAO if needed)
            vao = self._get_or_create_vao(obj, self.projector_shader)
            if vao is not None:
                vao.render(moderngl.TRIANGLES)

    def render_helpers(self, scene, camera):
        """Render helpers: grid, frustums, gizmos"""
        if not scene.show_helpers:
            return

        # Render grid
        if scene.show_grid and scene.grid:
            self._render_grid(scene.grid, camera)

        # Render projector frustums
        if scene.show_frustums:
            for projector in scene.get_active_projectors():
                self._render_frustum(projector, camera)

    def _render_grid(self, grid, camera):
        """Render grid lines"""
        # Grid parameters
        grid_size = 20  # 20x20 grid
        grid_spacing = 1.0
        half_size = grid_size * grid_spacing / 2.0

        # Grid color
        grid_color = (0.3, 0.3, 0.35)  # Subtle gray

        # Build grid lines
        start_positions = []
        end_positions = []

        # Lines along X axis
        for i in range(grid_size + 1):
            z = -half_size + i * grid_spacing
            start_positions.append((-half_size, 0, z))
            end_positions.append((half_size, 0, z))

        # Lines along Z axis
        for i in range(grid_size + 1):
            x = -half_size + i * grid_spacing
            start_positions.append((x, 0, -half_size))
            end_positions.append((x, 0, half_size))

        # Draw all grid lines
        self.draw_lines(start_positions, end_positions, grid_color, width=1.0, camera=camera)

    def _render_frustum(self, projector, camera):
        """Render projector frustum"""
        # Get frustum corners
        near_plane = projector.near
        far_plane = projector.far

        # Get FOV and aspect ratio
        fov_h = projector.get_fov()  # Horizontal FOV in degrees
        aspect = projector.aspect

        # Calculate half dimensions at near and far planes
        import math
        half_h_near = near_plane * math.tan(math.radians(fov_h / 2))
        half_v_near = half_h_near / aspect
        half_h_far = far_plane * math.tan(math.radians(fov_h / 2))
        half_v_far = half_h_far / aspect

        # Frustum corners in projector local space
        # Near plane
        ntr = np.array([half_h_near, half_v_near, -near_plane])
        ntl = np.array([-half_h_near, half_v_near, -near_plane])
        nbr = np.array([half_h_near, -half_v_near, -near_plane])
        nbl = np.array([-half_h_near, -half_v_near, -near_plane])

        # Far plane
        ftr = np.array([half_h_far, half_v_far, -far_plane])
        ftl = np.array([-half_h_far, half_v_far, -far_plane])
        fbr = np.array([half_h_far, -half_v_far, -far_plane])
        fbl = np.array([-half_h_far, -half_v_far, -far_plane])

        # Transform to world space
        transform = projector.get_model_matrix()

        def transform_point(p):
            p_h = np.append(p, 1.0)
            p_world = transform @ p_h
            return tuple(p_world[:3])

        ntr_w = transform_point(ntr)
        ntl_w = transform_point(ntl)
        nbr_w = transform_point(nbr)
        nbl_w = transform_point(nbl)
        ftr_w = transform_point(ftr)
        ftl_w = transform_point(ftl)
        fbr_w = transform_point(fbr)
        fbl_w = transform_point(fbl)

        # Build frustum lines
        start_positions = []
        end_positions = []

        # Near plane edges
        start_positions.extend([ntr_w, ntl_w, nbl_w, nbr_w])
        end_positions.extend([ntl_w, nbl_w, nbr_w, ntr_w])

        # Far plane edges
        start_positions.extend([ftr_w, ftl_w, fbl_w, fbr_w])
        end_positions.extend([ftl_w, fbl_w, fbr_w, ftr_w])

        # Connecting edges
        start_positions.extend([ntr_w, ntl_w, nbr_w, nbl_w])
        end_positions.extend([ftr_w, ftl_w, fbr_w, fbl_w])

        # Frustum color (yellow for active projector)
        frustum_color = (1.0, 0.8, 0.0) if projector.active else (0.5, 0.5, 0.5)

        # Draw frustum
        self.draw_lines(start_positions, end_positions, frustum_color, width=2.0, camera=camera)

    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        self.ctx.viewport = (0, 0, width, height)

    def cleanup(self):
        """Cleanup renderer resources"""
        # Release depth textures and framebuffers
        for tex in self.depth_textures:
            tex.release()
        for fbo in self.depth_framebuffers:
            fbo.release()

        # Release shaders
        self.depth_shader.release()
        self.projector_shader.release()
        self.line_shader.release()

        print("✅ Renderer cleaned up")
