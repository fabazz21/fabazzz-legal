"""
ModernGL Renderer
Handles all rendering: depth pass, main scene, helpers
"""

import moderngl
import numpy as np
from pathlib import Path
from core.line_renderer import LineRenderer


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

        # Line renderer for helpers (NEW: GPU-based line rendering)
        self.line_renderer = LineRenderer(self.ctx)

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
        """Render helpers: grid, axes using GPU LineRenderer"""
        if not scene.show_helpers:
            return

        lines = []

        # Add grid lines
        if scene.show_grid:
            for l in scene.grid:
                lines.append({
                    "start": tuple(l["start"]),
                    "end": tuple(l["end"]),
                    "color": tuple(l["color"])
                })

        # Add axis lines
        if scene.show_axes:
            for a in scene.axes:
                lines.append({
                    "start": tuple(a["start"]),
                    "end": tuple(a["end"]),
                    "color": tuple(a["color"])
                })

        # Draw all lines with GPU LineRenderer
        self.line_renderer.draw(lines, camera)

    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        self.ctx.viewport = (0, 0, width, height)

    def cleanup(self):
        """Cleanup renderer resources"""
        # Release line renderer
        self.line_renderer.release()

        # Release depth textures and framebuffers
        for tex in self.depth_textures:
            tex.release()
        for fbo in self.depth_framebuffers:
            fbo.release()

        # Release shaders
        self.depth_shader.release()
        self.projector_shader.release()

        print("✅ Renderer cleaned up")
