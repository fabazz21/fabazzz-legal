#version 330 core

// Depth Pass Fragment Shader
// Stores linear depth in red channel for shadow mapping

in float vDepth;

out vec4 FragColor;

void main() {
    // Store linear depth in red channel (replicated to RGB for debug visualization)
    FragColor = vec4(vDepth, vDepth, vDepth, 1.0);
}
