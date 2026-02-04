"""
GPU Line Renderer for grid, axes, gizmo
"""

import moderngl
import numpy as np
from pathlib import Path


class LineRenderer:
    """GPU Line Renderer for grid, axes, gizmo"""

    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        shader_path = Path(__file__).parent.parent / "shaders" / "line.glsl"
        src = shader_path.read_text()

        self.program = ctx.program(
            vertex_shader="#define VERTEX\n" + src,
            fragment_shader="#define FRAGMENT\n" + src,
        )

        self.vbo = None
        self.vao = None
        self.max_vertices = 0

    def draw(self, lines, camera):
        """
        Draw lines

        Args:
            lines: List of dicts with keys: start, end, color
                   Example: [{"start": (0,0,0), "end": (1,0,0), "color": (1,0,0)}]
            camera: Camera object with get_projection_matrix() and get_view_matrix()
        """
        if not lines:
            return

        # Build vertex buffer: pos + color
        data = []
        for l in lines:
            data.extend((*l["start"], *l["color"]))
            data.extend((*l["end"],   *l["color"]))

        vertex_data = np.array(data, dtype="f4")
        vertex_count = len(vertex_data) // 6

        if vertex_count == 0:
            return

        # Resize buffer if needed
        if self.vbo is None or vertex_count > self.max_vertices:
            if self.vbo:
                self.vbo.release()
            self.vbo = self.ctx.buffer(vertex_data.tobytes())
            self.max_vertices = vertex_count
        else:
            self.vbo.write(vertex_data.tobytes())

        if self.vao is None:
            self.vao = self.ctx.vertex_array(
                self.program,
                [(self.vbo, "3f 3f", "in_pos", "in_color")]
            )

        # MVP
        mvp = camera.get_projection_matrix() @ camera.get_view_matrix()
        self.program["u_mvp"].write(mvp.astype("f4").tobytes())

        # Draw
        self.ctx.disable(moderngl.CULL_FACE)
        self.vao.render(moderngl.LINES)
        self.ctx.enable(moderngl.CULL_FACE)

    def release(self):
        """Cleanup GPU resources"""
        if self.vbo:
            self.vbo.release()
        if self.vao:
            self.vao.release()
        self.program.release()
