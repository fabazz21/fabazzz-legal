#!/usr/bin/env python3
"""
MINIMAL WORKING VERSION - Just displays a rotating cube
"""

import sys
import moderngl
import glfw
import numpy as np
from pyrr import Matrix44


def main():
    print("=" * 60)
    print("  MINIMAL TEST - Rotating Cube")
    print("=" * 60)

    # Initialize GLFW
    if not glfw.init():
        print("❌ Failed to initialize GLFW")
        return 1

    # Create window
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "ModernGL Test", None, None)
    if not window:
        print("❌ Failed to create window")
        glfw.terminate()
        return 1

    glfw.make_context_current(window)
    print("✅ Window created: 1280x720")

    # Create ModernGL context
    ctx = moderngl.create_context(require=330)
    ctx.enable(moderngl.DEPTH_TEST)
    print(f"✅ OpenGL Version: {ctx.info.get('GL_VERSION', 'Unknown')}")

    # Simple vertex shader
    vertex_shader = """
    #version 330 core
    in vec3 in_position;
    uniform mat4 mvp;
    out vec3 vColor;

    void main() {
        gl_Position = mvp * vec4(in_position, 1.0);
        vColor = in_position * 0.5 + 0.5;  // Color based on position
    }
    """

    # Simple fragment shader
    fragment_shader = """
    #version 330 core
    in vec3 vColor;
    out vec4 FragColor;

    void main() {
        FragColor = vec4(vColor, 1.0);
    }
    """

    # Compile shader
    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    print("✅ Shader compiled")

    # Cube vertices
    vertices = np.array([
        # Front face
        -1, -1,  1,
         1, -1,  1,
         1,  1,  1,
        -1,  1,  1,
        # Back face
        -1, -1, -1,
        -1,  1, -1,
         1,  1, -1,
         1, -1, -1,
    ], dtype='f4')

    # Cube indices
    indices = np.array([
        0, 1, 2,  0, 2, 3,  # Front
        4, 5, 6,  4, 6, 7,  # Back
        0, 3, 5,  0, 5, 4,  # Left
        1, 7, 6,  1, 6, 2,  # Right
        3, 2, 6,  3, 6, 5,  # Top
        0, 4, 7,  0, 7, 1,  # Bottom
    ], dtype='i4')

    # Create buffers
    vbo = ctx.buffer(vertices.tobytes())
    ibo = ctx.buffer(indices.tobytes())
    vao = ctx.vertex_array(program, [(vbo, '3f', 'in_position')], ibo)
    print("✅ Cube created")

    # Animation
    rotation = 0.0

    print("\n🚀 Starting render loop...")
    print("   Press ESC to exit\n")

    frame_count = 0

    while not glfw.window_should_close(window):
        # Clear
        ctx.clear(0.1, 0.1, 0.15)

        # Update rotation
        rotation += 0.01

        # Create MVP matrix
        proj = Matrix44.perspective_projection(45.0, 1280/720, 0.1, 100.0)
        view = Matrix44.look_at(
            (np.sin(rotation) * 5, 3, np.cos(rotation) * 5),  # Eye position (rotating)
            (0, 0, 0),  # Look at center
            (0, 1, 0)   # Up vector
        )
        model = Matrix44.identity()
        mvp = proj * view * model

        # Set uniform
        program['mvp'].write(mvp.astype('f4').tobytes())

        # Render
        vao.render(moderngl.TRIANGLES)

        # Swap buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

        # Check ESC
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            break

        # FPS counter
        frame_count += 1
        if frame_count % 60 == 0:
            print(f"Frame {frame_count}")

    # Cleanup
    print("\n✅ Exiting...")
    glfw.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
