#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 fragPos;
out vec3 fragNormal;

void main() {
    fragPos = vec3(model * vec4(position, 1.0));
    fragNormal = normalize(mat3(model) * normal);
    gl_Position = projection * view * vec4(fragPos, 1.0);
}
