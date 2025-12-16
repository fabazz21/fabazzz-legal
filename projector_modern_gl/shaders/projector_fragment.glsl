#version 330 core

// Multi-Projector Fragment Shader with Shadow Mapping
// Supports up to 4 simultaneous projectors with:
// - Keystone correction (vertical/horizontal + 4-corner independent control)
// - Corner pin (homographic perspective transform)
// - Soft edge blending (per-edge gamma-controlled falloff)
// - Shadow mapping with depth comparison

precision highp float;

// Input from vertex shader
in vec3 vNormal;
in vec3 vWorldPos;
in vec4 vProjCoords0, vProjCoords1, vProjCoords2, vProjCoords3;
in vec4 vShadowCoord0, vShadowCoord1, vShadowCoord2, vShadowCoord3;

// Output
out vec4 FragColor;

// Scene lighting
uniform vec3 baseColor;
uniform vec3 dirLightDir;
uniform float ambientLightIntensity;
uniform float directionalLightIntensity;

// Projector textures and settings
uniform sampler2D projTexture0, projTexture1, projTexture2, projTexture3;
uniform vec3 projPosition0, projPosition1, projPosition2, projPosition3;
uniform bool hasTexture0, hasTexture1, hasTexture2, hasTexture3;
uniform float intensity0, intensity1, intensity2, intensity3;
uniform bool projectorActive0, projectorActive1, projectorActive2, projectorActive3;

// Shadow maps
uniform sampler2D shadowMap0, shadowMap1, shadowMap2, shadowMap3;
uniform mat4 shadowViewMatrix0, shadowViewMatrix1, shadowViewMatrix2, shadowViewMatrix3;
uniform float shadowBias0, shadowBias1, shadowBias2, shadowBias3;
uniform float depthMapFar0, depthMapFar1, depthMapFar2, depthMapFar3;
uniform float projectionFar0, projectionFar1, projectionFar2, projectionFar3;

// Keystone uniforms (vertical/horizontal + 4 corners with X/Y control)
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

// Soft edge uniforms (L/R/T/B + gamma)
uniform float softEdgeL0, softEdgeR0, softEdgeT0, softEdgeB0, softEdgeGamma0;
uniform float softEdgeL1, softEdgeR1, softEdgeT1, softEdgeB1, softEdgeGamma1;
uniform float softEdgeL2, softEdgeR2, softEdgeT2, softEdgeB2, softEdgeGamma2;
uniform float softEdgeL3, softEdgeR3, softEdgeT3, softEdgeB3, softEdgeGamma3;

// Corner Pin uniforms (independent XY control for all 4 corners)
uniform float cornerPinTLX0, cornerPinTLY0, cornerPinTRX0, cornerPinTRY0;
uniform float cornerPinBLX0, cornerPinBLY0, cornerPinBRX0, cornerPinBRY0;
uniform float cornerPinTLX1, cornerPinTLY1, cornerPinTRX1, cornerPinTRY1;
uniform float cornerPinBLX1, cornerPinBLY1, cornerPinBRX1, cornerPinBRY1;
uniform float cornerPinTLX2, cornerPinTLY2, cornerPinTRX2, cornerPinTRY2;
uniform float cornerPinBLX2, cornerPinBLY2, cornerPinBRX2, cornerPinBRY2;
uniform float cornerPinTLX3, cornerPinTLY3, cornerPinTRX3, cornerPinTRY3;
uniform float cornerPinBLX3, cornerPinBLY3, cornerPinBRX3, cornerPinBRY3;

// ============================================================================
// KEYSTONE CORRECTION
// ============================================================================
// Keystone: Define trapezoid corners and check if point is inside
// Returns: vec4(textureUV.xy, isInside, 0)
vec4 applyKeystoneWithBounds(vec2 uv, float kV, float kH,
    float kTLX, float kTLY, float kTRX, float kTRY,
    float kBLX, float kBLY, float kBRX, float kBRY) {

    // Scale factors for keystone parameters
    float scale = 0.005;
    float cornerScale = 0.01;  // 1% per unit for corners (more amplitude)

    // Define trapezoid corners with INDEPENDENT X and Y control
    // Bottom-left corner
    vec2 bl = vec2(
        -kV * scale + kBLX * cornerScale,     // X: kV + independent X control
        -kH * scale + kBLY * cornerScale      // Y: kH + independent Y control
    );

    // Bottom-right corner
    vec2 br = vec2(
        1.0 + kV * scale + kBRX * cornerScale,  // X: kV + independent X control
        kH * scale + kBRY * cornerScale         // Y: kH + independent Y control
    );

    // Top-left corner
    vec2 tl = vec2(
        kV * scale + kTLX * cornerScale,        // X: kV + independent X control
        1.0 + kH * scale + kTLY * cornerScale   // Y: kH + independent Y control
    );

    // Top-right corner
    vec2 tr = vec2(
        1.0 - kV * scale + kTRX * cornerScale,  // X: kV + independent X control
        1.0 - kH * scale + kTRY * cornerScale   // Y: kH + independent Y control
    );

    // Check if UV point is inside the trapezoid using cross product method
    // For a convex quad, point is inside if it's on the same side of all edges
    vec2 v0 = br - bl;
    vec2 v1 = tr - br;
    vec2 v2 = tl - tr;
    vec2 v3 = bl - tl;

    vec2 p0 = uv - bl;
    vec2 p1 = uv - br;
    vec2 p2 = uv - tr;
    vec2 p3 = uv - tl;

    float c0 = v0.x * p0.y - v0.y * p0.x;
    float c1 = v1.x * p1.y - v1.y * p1.x;
    float c2 = v2.x * p2.y - v2.y * p2.x;
    float c3 = v3.x * p3.y - v3.y * p3.x;

    // Point is inside if all cross products have the same sign
    bool inside = (c0 >= 0.0 && c1 >= 0.0 && c2 >= 0.0 && c3 >= 0.0) ||
                  (c0 <= 0.0 && c1 <= 0.0 && c2 <= 0.0 && c3 <= 0.0);

    if (!inside) {
        return vec4(0.0, 0.0, 0.0, 0.0);
    }

    // Inverse bilinear interpolation: find (s,t) such that
    // P = (1-t)*[(1-s)*bl + s*br] + t*[(1-s)*tl + s*tr]
    // This maps the trapezoid back to the unit square for texture sampling

    vec2 e = br - bl;
    vec2 f = tl - bl;
    vec2 g = bl - br + tr - tl;
    vec2 h = uv - bl;

    // Solve quadratic for t: (g×f)t² + (e×f + h×g)t + h×e = 0
    // where × denotes 2D cross product (a×b = a.x*b.y - a.y*b.x)
    float gxf = g.x * f.y - g.y * f.x;
    float exf = e.x * f.y - e.y * f.x;
    float hxg = h.x * g.y - h.y * g.x;
    float hxe = h.x * e.y - h.y * e.x;

    float t;
    if (abs(gxf) < 0.0001) {
        // Linear case
        t = -hxe / (exf + hxg);
    } else {
        // Quadratic case
        float a = gxf;
        float b = exf + hxg;
        float c = hxe;
        float disc = b * b - 4.0 * a * c;
        if (disc < 0.0) {
            return vec4(0.0, 0.0, 0.0, 0.0);
        }
        float sqrtDisc = sqrt(disc);
        float t1 = (-b - sqrtDisc) / (2.0 * a);
        float t2 = (-b + sqrtDisc) / (2.0 * a);
        t = (t1 >= 0.0 && t1 <= 1.0) ? t1 : t2;
    }

    // Compute s from t
    vec2 leftEdge = mix(bl, tl, t);
    vec2 rightEdge = mix(br, tr, t);
    vec2 edgeVec = rightEdge - leftEdge;
    vec2 toPoint = uv - leftEdge;

    float s;
    if (abs(edgeVec.x) > abs(edgeVec.y)) {
        s = toPoint.x / edgeVec.x;
    } else {
        s = toPoint.y / edgeVec.y;
    }

    // Clamp to valid range
    s = clamp(s, 0.0, 1.0);
    t = clamp(t, 0.0, 1.0);

    return vec4(s, t, 1.0, 0.0);
}

// ============================================================================
// CORNER PIN CORRECTION
// ============================================================================
// Corner Pin Correction using Homography (Perspective Transform)
// More precise than keystone - allows independent corner manipulation
vec4 applyCornerPin(vec2 uv,
    float cpTLX, float cpTLY, float cpTRX, float cpTRY,
    float cpBLX, float cpBLY, float cpBRX, float cpBRY) {

    // Same algorithm as Keystone, but with individual corner control
    // Scale from percentage (-100 to +100) to normalized coordinates
    float scale = 0.01;  // 1% per unit

    // Define quad corners (same logic as Keystone)
    vec2 tl = vec2(0.0 + cpTLX * scale, 0.0 + cpTLY * scale);
    vec2 tr = vec2(1.0 + cpTRX * scale, 0.0 + cpTRY * scale);
    vec2 bl = vec2(0.0 + cpBLX * scale, 1.0 + cpBLY * scale);
    vec2 br = vec2(1.0 + cpBRX * scale, 1.0 + cpBRY * scale);

    // Check if UV point is inside the quad (same as Keystone)
    vec2 v0 = br - bl;
    vec2 v1 = tr - br;
    vec2 v2 = tl - tr;
    vec2 v3 = bl - tl;

    vec2 p0 = uv - bl;
    vec2 p1 = uv - br;
    vec2 p2 = uv - tr;
    vec2 p3 = uv - tl;

    float c0 = v0.x * p0.y - v0.y * p0.x;
    float c1 = v1.x * p1.y - v1.y * p1.x;
    float c2 = v2.x * p2.y - v2.y * p2.x;
    float c3 = v3.x * p3.y - v3.y * p3.x;

    bool inside = (c0 >= 0.0 && c1 >= 0.0 && c2 >= 0.0 && c3 >= 0.0) ||
                  (c0 <= 0.0 && c1 <= 0.0 && c2 <= 0.0 && c3 <= 0.0);

    if (!inside) {
        return vec4(0.0, 0.0, 0.0, 0.0);
    }

    // Inverse bilinear interpolation (same as Keystone)
    vec2 e = br - bl;
    vec2 f = tl - bl;
    vec2 g = bl - br + tr - tl;
    vec2 h = uv - bl;

    float gxf = g.x * f.y - g.y * f.x;
    float exf = e.x * f.y - e.y * f.x;
    float hxg = h.x * g.y - h.y * g.x;
    float hxe = h.x * e.y - h.y * e.x;

    float t;
    if (abs(gxf) < 0.0001) {
        t = -hxe / (exf + hxg);
    } else {
        float a = gxf;
        float b = exf + hxg;
        float c = hxe;
        float disc = b * b - 4.0 * a * c;
        if (disc < 0.0) {
            return vec4(0.0, 0.0, 0.0, 0.0);
        }
        float sqrtDisc = sqrt(disc);
        float t1 = (-b - sqrtDisc) / (2.0 * a);
        float t2 = (-b + sqrtDisc) / (2.0 * a);
        t = (t1 >= 0.0 && t1 <= 1.0) ? t1 : t2;
    }

    vec2 leftEdge = mix(bl, tl, t);
    vec2 rightEdge = mix(br, tr, t);
    vec2 edgeVec = rightEdge - leftEdge;
    vec2 toPoint = uv - leftEdge;

    float s;
    if (abs(edgeVec.x) > abs(edgeVec.y)) {
        s = toPoint.x / edgeVec.x;
    } else {
        s = toPoint.y / edgeVec.y;
    }

    s = clamp(s, 0.0, 1.0);
    t = clamp(t, 0.0, 1.0);

    return vec4(s, t, 1.0, 0.0);
}

// ============================================================================
// SOFT EDGE BLENDING
// ============================================================================
// Apply soft edge blending with gamma-controlled falloff
float applySoftEdge(vec2 uv, float edgeL, float edgeR, float edgeT, float edgeB, float gamma) {
    float blend = 1.0;

    // Left edge
    if (edgeL > 0.0) {
        float edgeWidth = edgeL / 100.0;
        if (uv.x < edgeWidth) {
            blend *= pow(uv.x / edgeWidth, 1.0 / gamma);
        }
    }

    // Right edge
    if (edgeR > 0.0) {
        float edgeWidth = edgeR / 100.0;
        if (uv.x > 1.0 - edgeWidth) {
            blend *= pow((1.0 - uv.x) / edgeWidth, 1.0 / gamma);
        }
    }

    // Top edge
    if (edgeT > 0.0) {
        float edgeWidth = edgeT / 100.0;
        if (uv.y < edgeWidth) {
            blend *= pow(uv.y / edgeWidth, 1.0 / gamma);
        }
    }

    // Bottom edge
    if (edgeB > 0.0) {
        float edgeWidth = edgeB / 100.0;
        if (uv.y > 1.0 - edgeWidth) {
            blend *= pow((1.0 - uv.y) / edgeWidth, 1.0 / gamma);
        }
    }

    return clamp(blend, 0.0, 1.0);
}

// ============================================================================
// MAIN FRAGMENT SHADER
// ============================================================================
void main() {
    vec3 normal = normalize(vNormal);
    float NdotL = abs(dot(normal, normalize(dirLightDir)));

    // Lighting calculation
    float ambientComponent = ambientLightIntensity;
    float directionalComponent = directionalLightIntensity * NdotL;
    float lighting = ambientComponent + directionalComponent;

    // Start with baseColor
    vec3 color = baseColor * lighting;

    // ==================================================
    // PROJECTOR 0
    // ==================================================
    if (projectorActive0) {
        vec3 pCoord = vProjCoords0.xyz / vProjCoords0.w;
        vec2 uv = pCoord.xy * 0.5 + 0.5;

        if (pCoord.z >= 0.0 && pCoord.z <= 1.0) {
            // Apply keystone
            vec4 keystoneResult = applyKeystoneWithBounds(uv, keystoneV0, keystoneH0,
                keystoneTLX0, keystoneTLY0, keystoneTRX0, keystoneTRY0,
                keystoneBLX0, keystoneBLY0, keystoneBRX0, keystoneBRY0);

            if (keystoneResult.z > 0.5) {
                vec2 textureUV = keystoneResult.xy;

                // Apply corner pin AFTER keystone
                vec4 cornerPinResult = applyCornerPin(textureUV,
                    cornerPinTLX0, cornerPinTLY0, cornerPinTRX0, cornerPinTRY0,
                    cornerPinBLX0, cornerPinBLY0, cornerPinBRX0, cornerPinBRY0);

                if (cornerPinResult.z > 0.5) {
                    textureUV = cornerPinResult.xy;
                }

                vec3 lightDir = normalize(projPosition0 - vWorldPos);
                float facing = max(dot(normal, lightDir), 0.25);
                float dist = length(projPosition0 - vWorldPos);
                float distAtten = 1.0 - smoothstep(projectionFar0 * 0.7, projectionFar0, dist);

                // Soft edge blending
                float softEdgeBlend = applySoftEdge(textureUV, softEdgeL0, softEdgeR0, softEdgeT0, softEdgeB0, softEdgeGamma0);

                // Shadow check
                vec3 sCoord = vShadowCoord0.xyz / vShadowCoord0.w;
                sCoord = sCoord * 0.5 + 0.5;
                float shadow = 1.0;
                if (sCoord.x >= 0.0 && sCoord.x <= 1.0 && sCoord.y >= 0.0 && sCoord.y <= 1.0) {
                    vec4 viewPos = shadowViewMatrix0 * vec4(vWorldPos, 1.0);
                    float currentDepth = (-viewPos.z - 0.1) / (depthMapFar0 - 0.1);
                    float storedDepth = texture(shadowMap0, sCoord.xy).r;
                    if (storedDepth > 0.001 && storedDepth < 0.999) {
                        shadow = step(currentDepth, storedDepth + shadowBias0);
                    }
                }

                float projMix = intensity0 * facing * distAtten * shadow * softEdgeBlend;

                if (hasTexture0) {
                    vec4 texC = texture(projTexture0, textureUV);
                    color += texC.rgb * projMix;
                }
            }
        }
    }

    // ==================================================
    // PROJECTOR 1  (Same logic, different uniforms)
    // ==================================================
    if (projectorActive1) {
        vec3 pCoord = vProjCoords1.xyz / vProjCoords1.w;
        vec2 uv = pCoord.xy * 0.5 + 0.5;

        if (pCoord.z >= 0.0 && pCoord.z <= 1.0) {
            vec4 keystoneResult = applyKeystoneWithBounds(uv, keystoneV1, keystoneH1,
                keystoneTLX1, keystoneTLY1, keystoneTRX1, keystoneTRY1,
                keystoneBLX1, keystoneBLY1, keystoneBRX1, keystoneBRY1);

            if (keystoneResult.z > 0.5) {
                vec2 textureUV = keystoneResult.xy;

                vec4 cornerPinResult = applyCornerPin(textureUV,
                    cornerPinTLX1, cornerPinTLY1, cornerPinTRX1, cornerPinTRY1,
                    cornerPinBLX1, cornerPinBLY1, cornerPinBRX1, cornerPinBRY1);

                if (cornerPinResult.z > 0.5) {
                    textureUV = cornerPinResult.xy;
                }

                vec3 lightDir = normalize(projPosition1 - vWorldPos);
                float facing = max(dot(normal, lightDir), 0.25);
                float dist = length(projPosition1 - vWorldPos);
                float distAtten = 1.0 - smoothstep(projectionFar1 * 0.7, projectionFar1, dist);

                float softEdgeBlend = applySoftEdge(textureUV, softEdgeL1, softEdgeR1, softEdgeT1, softEdgeB1, softEdgeGamma1);

                vec3 sCoord = vShadowCoord1.xyz / vShadowCoord1.w;
                sCoord = sCoord * 0.5 + 0.5;
                float shadow = 1.0;
                if (sCoord.x >= 0.0 && sCoord.x <= 1.0 && sCoord.y >= 0.0 && sCoord.y <= 1.0) {
                    vec4 viewPos = shadowViewMatrix1 * vec4(vWorldPos, 1.0);
                    float currentDepth = (-viewPos.z - 0.1) / (depthMapFar1 - 0.1);
                    float storedDepth = texture(shadowMap1, sCoord.xy).r;
                    if (storedDepth > 0.001 && storedDepth < 0.999) {
                        shadow = step(currentDepth, storedDepth + shadowBias1);
                    }
                }

                float projMix = intensity1 * facing * distAtten * shadow * softEdgeBlend;

                if (hasTexture1) {
                    vec4 texC = texture(projTexture1, textureUV);
                    color += texC.rgb * projMix;
                }
            }
        }
    }

    // ==================================================
    // PROJECTOR 2 (Same logic)
    // ==================================================
    if (projectorActive2) {
        vec3 pCoord = vProjCoords2.xyz / vProjCoords2.w;
        vec2 uv = pCoord.xy * 0.5 + 0.5;

        if (pCoord.z >= 0.0 && pCoord.z <= 1.0) {
            vec4 keystoneResult = applyKeystoneWithBounds(uv, keystoneV2, keystoneH2,
                keystoneTLX2, keystoneTLY2, keystoneTRX2, keystoneTRY2,
                keystoneBLX2, keystoneBLY2, keystoneBRX2, keystoneBRY2);

            if (keystoneResult.z > 0.5) {
                vec2 textureUV = keystoneResult.xy;

                vec4 cornerPinResult = applyCornerPin(textureUV,
                    cornerPinTLX2, cornerPinTLY2, cornerPinTRX2, cornerPinTRY2,
                    cornerPinBLX2, cornerPinBLY2, cornerPinBRX2, cornerPinBRY2);

                if (cornerPinResult.z > 0.5) {
                    textureUV = cornerPinResult.xy;
                }

                vec3 lightDir = normalize(projPosition2 - vWorldPos);
                float facing = max(dot(normal, lightDir), 0.25);
                float dist = length(projPosition2 - vWorldPos);
                float distAtten = 1.0 - smoothstep(projectionFar2 * 0.7, projectionFar2, dist);

                float softEdgeBlend = applySoftEdge(textureUV, softEdgeL2, softEdgeR2, softEdgeT2, softEdgeB2, softEdgeGamma2);

                vec3 sCoord = vShadowCoord2.xyz / vShadowCoord2.w;
                sCoord = sCoord * 0.5 + 0.5;
                float shadow = 1.0;
                if (sCoord.x >= 0.0 && sCoord.x <= 1.0 && sCoord.y >= 0.0 && sCoord.y <= 1.0) {
                    vec4 viewPos = shadowViewMatrix2 * vec4(vWorldPos, 1.0);
                    float currentDepth = (-viewPos.z - 0.1) / (depthMapFar2 - 0.1);
                    float storedDepth = texture(shadowMap2, sCoord.xy).r;
                    if (storedDepth > 0.001 && storedDepth < 0.999) {
                        shadow = step(currentDepth, storedDepth + shadowBias2);
                    }
                }

                float projMix = intensity2 * facing * distAtten * shadow * softEdgeBlend;

                if (hasTexture2) {
                    vec4 texC = texture(projTexture2, textureUV);
                    color += texC.rgb * projMix;
                }
            }
        }
    }

    // ==================================================
    // PROJECTOR 3 (Same logic)
    // ==================================================
    if (projectorActive3) {
        vec3 pCoord = vProjCoords3.xyz / vProjCoords3.w;
        vec2 uv = pCoord.xy * 0.5 + 0.5;

        if (pCoord.z >= 0.0 && pCoord.z <= 1.0) {
            vec4 keystoneResult = applyKeystoneWithBounds(uv, keystoneV3, keystoneH3,
                keystoneTLX3, keystoneTLY3, keystoneTRX3, keystoneTRY3,
                keystoneBLX3, keystoneBLY3, keystoneBRX3, keystoneBRY3);

            if (keystoneResult.z > 0.5) {
                vec2 textureUV = keystoneResult.xy;

                vec4 cornerPinResult = applyCornerPin(textureUV,
                    cornerPinTLX3, cornerPinTLY3, cornerPinTRX3, cornerPinTRY3,
                    cornerPinBLX3, cornerPinBLY3, cornerPinBRX3, cornerPinBRY3);

                if (cornerPinResult.z > 0.5) {
                    textureUV = cornerPinResult.xy;
                }

                vec3 lightDir = normalize(projPosition3 - vWorldPos);
                float facing = max(dot(normal, lightDir), 0.25);
                float dist = length(projPosition3 - vWorldPos);
                float distAtten = 1.0 - smoothstep(projectionFar3 * 0.7, projectionFar3, dist);

                float softEdgeBlend = applySoftEdge(textureUV, softEdgeL3, softEdgeR3, softEdgeT3, softEdgeB3, softEdgeGamma3);

                vec3 sCoord = vShadowCoord3.xyz / vShadowCoord3.w;
                sCoord = sCoord * 0.5 + 0.5;
                float shadow = 1.0;
                if (sCoord.x >= 0.0 && sCoord.x <= 1.0 && sCoord.y >= 0.0 && sCoord.y <= 1.0) {
                    vec4 viewPos = shadowViewMatrix3 * vec4(vWorldPos, 1.0);
                    float currentDepth = (-viewPos.z - 0.1) / (depthMapFar3 - 0.1);
                    float storedDepth = texture(shadowMap3, sCoord.xy).r;
                    if (storedDepth > 0.001 && storedDepth < 0.999) {
                        shadow = step(currentDepth, storedDepth + shadowBias3);
                    }
                }

                float projMix = intensity3 * facing * distAtten * shadow * softEdgeBlend;

                if (hasTexture3) {
                    vec4 texC = texture(projTexture3, textureUV);
                    color += texC.rgb * projMix;
                }
            }
        }
    }

    // Final output
    FragColor = vec4(color, 1.0);
}
