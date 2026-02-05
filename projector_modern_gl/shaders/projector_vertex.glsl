#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat3 normalMatrix;

// Projector matrices (up to 4 projectors)
uniform mat4 projMatrix0;
uniform mat4 projMatrix1;
uniform mat4 projMatrix2;
uniform mat4 projMatrix3;

uniform mat4 shadowMatrix0;
uniform mat4 shadowMatrix1;
uniform mat4 shadowMatrix2;
uniform mat4 shadowMatrix3;

out vec3 v_fragPos;
out vec3 v_normal;
out vec4 v_projCoord0;
out vec4 v_projCoord1;
out vec4 v_projCoord2;
out vec4 v_projCoord3;
out vec4 v_shadowCoord0;
out vec4 v_shadowCoord1;
out vec4 v_shadowCoord2;
out vec4 v_shadowCoord3;

void main() {
    vec4 worldPos = model * vec4(in_position, 1.0);
    v_fragPos = worldPos.xyz;
    v_normal = normalize(normalMatrix * in_normal);

    gl_Position = projection * view * worldPos;

    // Calculate projection coordinates for each projector
    v_projCoord0 = projMatrix0 * worldPos;
    v_projCoord1 = projMatrix1 * worldPos;
    v_projCoord2 = projMatrix2 * worldPos;
    v_projCoord3 = projMatrix3 * worldPos;

    // Calculate shadow coordinates
    v_shadowCoord0 = shadowMatrix0 * worldPos;
    v_shadowCoord1 = shadowMatrix1 * worldPos;
    v_shadowCoord2 = shadowMatrix2 * worldPos;
    v_shadowCoord3 = shadowMatrix3 * worldPos;
}
