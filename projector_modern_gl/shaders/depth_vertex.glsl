#version 330 core

layout (location = 0) in vec3 in_position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out float v_depth;

void main() {
    vec4 viewPos = view * model * vec4(in_position, 1.0);
    gl_Position = projection * viewPos;

    // Linear depth
    v_depth = -viewPos.z;
}
