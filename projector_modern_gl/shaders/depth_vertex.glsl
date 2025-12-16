#version 330 core

// Depth Pass Vertex Shader
// Renders linear depth from projector's point of view for shadow mapping

in vec3 in_position;

out float vDepth;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float cameraNear;
uniform float cameraFar;

void main() {
    vec4 mvPosition = view * model * vec4(in_position, 1.0);

    // Linear depth normalized to [0, 1]
    vDepth = (-mvPosition.z - cameraNear) / (cameraFar - cameraNear);

    gl_Position = projection * mvPosition;
}
