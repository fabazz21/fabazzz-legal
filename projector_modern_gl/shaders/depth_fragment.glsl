#version 330 core

in float v_depth;

uniform float cameraNear;
uniform float cameraFar;

out float fragColor;

void main() {
    // Normalize depth to [0, 1] range
    float normalizedDepth = (v_depth - cameraNear) / (cameraFar - cameraNear);
    fragColor = clamp(normalizedDepth, 0.0, 1.0);
}
