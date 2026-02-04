#version 330 core

#ifdef VERTEX
layout (location = 0) in vec3 in_pos;
layout (location = 1) in vec3 in_color;

uniform mat4 u_mvp;

out vec3 v_color;

void main() {
    v_color = in_color;
    gl_Position = u_mvp * vec4(in_pos, 1.0);
}
#endif

#ifdef FRAGMENT
in vec3 v_color;
out vec4 fragColor;

void main() {
    fragColor = vec4(v_color, 1.0);
}
#endif
