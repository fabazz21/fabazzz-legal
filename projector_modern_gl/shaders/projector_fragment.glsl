#version 330 core

in vec3 v_fragPos;
in vec3 v_normal;
in vec4 v_projCoord0;
in vec4 v_projCoord1;
in vec4 v_projCoord2;
in vec4 v_projCoord3;
in vec4 v_shadowCoord0;
in vec4 v_shadowCoord1;
in vec4 v_shadowCoord2;
in vec4 v_shadowCoord3;

// Base material
uniform vec3 baseColor;

// Lighting
uniform vec3 dirLightDir;
uniform float ambientLightIntensity;
uniform float directionalLightIntensity;

// Projectors (up to 4)
uniform bool projectorActive0;
uniform bool projectorActive1;
uniform bool projectorActive2;
uniform bool projectorActive3;

uniform vec3 projPosition0;
uniform vec3 projPosition1;
uniform vec3 projPosition2;
uniform vec3 projPosition3;

uniform float intensity0;
uniform float intensity1;
uniform float intensity2;
uniform float intensity3;

uniform bool hasTexture0;
uniform bool hasTexture1;
uniform bool hasTexture2;
uniform bool hasTexture3;

uniform sampler2D projTexture0;
uniform sampler2D projTexture1;
uniform sampler2D projTexture2;
uniform sampler2D projTexture3;

uniform sampler2D shadowMap0;
uniform sampler2D shadowMap1;
uniform sampler2D shadowMap2;
uniform sampler2D shadowMap3;

uniform mat4 shadowViewMatrix0;
uniform mat4 shadowViewMatrix1;
uniform mat4 shadowViewMatrix2;
uniform mat4 shadowViewMatrix3;

uniform float shadowBias0;
uniform float shadowBias1;
uniform float shadowBias2;
uniform float shadowBias3;

uniform float depthMapFar0;
uniform float depthMapFar1;
uniform float depthMapFar2;
uniform float depthMapFar3;

uniform float projectionFar0;
uniform float projectionFar1;
uniform float projectionFar2;
uniform float projectionFar3;

// Keystone correction
uniform float keystoneV0, keystoneH0;
uniform float keystoneTLX0, keystoneTLY0, keystoneTRX0, keystoneTRY0;
uniform float keystoneBLX0, keystoneBLY0, keystoneBRX0, keystoneBRY0;

uniform float keystoneV1, keystoneH1;
uniform float keystoneTLX1, keystoneTLY1, keystoneTRX1, keystoneTRY1;
uniform float keystoneBLX1, keystoneBLY1, keystoneBRX1, keystoneBRY1;

uniform float keystoneV2, keystoneH2;
uniform float keystoneTLX2, keystoneTLY2, keystoneTRX2, keystoneTRY2;
uniform float keystoneBLX2, keystoneBLY2, keystoneBRX2, keystoneBRY2;

uniform float keystoneV3, keystoneH3;
uniform float keystoneTLX3, keystoneTLY3, keystoneTRX3, keystoneTRY3;
uniform float keystoneBLX3, keystoneBLY3, keystoneBRX3, keystoneBRY3;

// Soft edge blending
uniform float softEdgeL0, softEdgeR0, softEdgeT0, softEdgeB0, softEdgeGamma0;
uniform float softEdgeL1, softEdgeR1, softEdgeT1, softEdgeB1, softEdgeGamma1;
uniform float softEdgeL2, softEdgeR2, softEdgeT2, softEdgeB2, softEdgeGamma2;
uniform float softEdgeL3, softEdgeR3, softEdgeT3, softEdgeB3, softEdgeGamma3;

// Corner pin
uniform float cornerPinTLX0, cornerPinTLY0, cornerPinTRX0, cornerPinTRY0;
uniform float cornerPinBLX0, cornerPinBLY0, cornerPinBRX0, cornerPinBRY0;

uniform float cornerPinTLX1, cornerPinTLY1, cornerPinTRX1, cornerPinTRY1;
uniform float cornerPinBLX1, cornerPinBLY1, cornerPinBRX1, cornerPinBRY1;

uniform float cornerPinTLX2, cornerPinTLY2, cornerPinTRX2, cornerPinTRY2;
uniform float cornerPinBLX2, cornerPinBLY2, cornerPinBRX2, cornerPinBRY2;

uniform float cornerPinTLX3, cornerPinTLY3, cornerPinTRX3, cornerPinTRY3;
uniform float cornerPinBLX3, cornerPinBLY3, cornerPinBRX3, cornerPinBRY3;

out vec4 fragColor;

// Calculate soft edge blending
float softEdgeBlend(vec2 uv, float l, float r, float t, float b, float gamma) {
    float blendX = 1.0;
    float blendY = 1.0;

    if (uv.x < l) {
        blendX = pow(uv.x / l, gamma);
    } else if (uv.x > (1.0 - r)) {
        blendX = pow((1.0 - uv.x) / r, gamma);
    }

    if (uv.y < b) {
        blendY = pow(uv.y / b, gamma);
    } else if (uv.y > (1.0 - t)) {
        blendY = pow((1.0 - uv.y) / t, gamma);
    }

    return blendX * blendY;
}

// Calculate shadow
float calculateShadow(vec4 shadowCoord, sampler2D shadowMap, float bias) {
    // Perspective divide
    vec3 projCoords = shadowCoord.xyz / shadowCoord.w;

    // Check if in shadow map bounds
    if (projCoords.x < 0.0 || projCoords.x > 1.0 ||
        projCoords.y < 0.0 || projCoords.y > 1.0 ||
        projCoords.z < 0.0 || projCoords.z > 1.0) {
        return 1.0;
    }

    // Get depth from shadow map
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;

    // Shadow test
    float shadow = currentDepth - bias > closestDepth ? 0.0 : 1.0;

    return shadow;
}

// Process single projector
vec3 processProjector(
    bool active,
    vec4 projCoord,
    vec4 shadowCoord,
    vec3 projPos,
    float intensity,
    bool hasTexture,
    sampler2D projTex,
    sampler2D shadowMap,
    float shadowBias,
    float softL, float softR, float softT, float softB, float softGamma
) {
    if (!active) {
        return vec3(0.0);
    }

    // Perspective divide
    vec3 projUV = projCoord.xyz / projCoord.w;

    // Check if fragment is within projector frustum
    if (projUV.x < 0.0 || projUV.x > 1.0 ||
        projUV.y < 0.0 || projUV.y > 1.0 ||
        projUV.z < 0.0 || projUV.z > 1.0) {
        return vec3(0.0);
    }

    // Calculate shadow
    float shadow = calculateShadow(shadowCoord, shadowMap, shadowBias);

    // Soft edge blending
    float softEdge = softEdgeBlend(projUV.xy, softL, softR, softT, softB, softGamma);

    // Sample texture
    vec3 projColor = vec3(1.0);
    if (hasTexture) {
        projColor = texture(projTex, projUV.xy).rgb;
    }

    // Combine
    return projColor * intensity * shadow * softEdge;
}

void main() {
    // Base lighting
    vec3 normal = normalize(v_normal);
    float diffuse = max(dot(normal, -dirLightDir), 0.0);
    vec3 lighting = vec3(ambientLightIntensity + directionalLightIntensity * diffuse);
    vec3 finalColor = baseColor * lighting;

    // Projector 0
    vec3 proj0 = processProjector(
        projectorActive0, v_projCoord0, v_shadowCoord0, projPosition0,
        intensity0, hasTexture0, projTexture0, shadowMap0, shadowBias0,
        softEdgeL0, softEdgeR0, softEdgeT0, softEdgeB0, softEdgeGamma0
    );
    finalColor += proj0;

    // Projector 1
    vec3 proj1 = processProjector(
        projectorActive1, v_projCoord1, v_shadowCoord1, projPosition1,
        intensity1, hasTexture1, projTexture1, shadowMap1, shadowBias1,
        softEdgeL1, softEdgeR1, softEdgeT1, softEdgeB1, softEdgeGamma1
    );
    finalColor += proj1;

    // Projector 2
    vec3 proj2 = processProjector(
        projectorActive2, v_projCoord2, v_shadowCoord2, projPosition2,
        intensity2, hasTexture2, projTexture2, shadowMap2, shadowBias2,
        softEdgeL2, softEdgeR2, softEdgeT2, softEdgeB2, softEdgeGamma2
    );
    finalColor += proj2;

    // Projector 3
    vec3 proj3 = processProjector(
        projectorActive3, v_projCoord3, v_shadowCoord3, projPosition3,
        intensity3, hasTexture3, projTexture3, shadowMap3, shadowBias3,
        softEdgeL3, softEdgeR3, softEdgeT3, softEdgeB3, softEdgeGamma3
    );
    finalColor += proj3;

    fragColor = vec4(finalColor, 1.0);
}
