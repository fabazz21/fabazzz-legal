#version 330 core

// Multi-Projector Vertex Shader
// Handles up to 4 simultaneous projectors with shadow mapping

in vec3 in_position;
in vec3 in_normal;

out vec3 vNormal;
out vec3 vWorldPos;
out vec4 vProjCoords0, vProjCoords1, vProjCoords2, vProjCoords3;
out vec4 vShadowCoord0, vShadowCoord1, vShadowCoord2, vShadowCoord3;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat3 normalMatrix;

// Projection matrices for each projector
uniform mat4 projMatrix0, projMatrix1, projMatrix2, projMatrix3;
uniform mat4 shadowMatrix0, shadowMatrix1, shadowMatrix2, shadowMatrix3;

void main() {
    // Transform normal to world space
    vNormal = normalize(normalMatrix * in_normal);

    // Transform position to world space
    vec4 worldPosition = model * vec4(in_position, 1.0);
    vWorldPos = worldPosition.xyz;

    // Calculate projection coordinates for each projector
    vProjCoords0 = projMatrix0 * worldPosition;
    vProjCoords1 = projMatrix1 * worldPosition;
    vProjCoords2 = projMatrix2 * worldPosition;
    vProjCoords3 = projMatrix3 * worldPosition;

    // Calculate shadow coordinates for each projector
    vShadowCoord0 = shadowMatrix0 * worldPosition;
    vShadowCoord1 = shadowMatrix1 * worldPosition;
    vShadowCoord2 = shadowMatrix2 * worldPosition;
    vShadowCoord3 = shadowMatrix3 * worldPosition;

    // Final position
    gl_Position = projection * view * worldPosition;
}
