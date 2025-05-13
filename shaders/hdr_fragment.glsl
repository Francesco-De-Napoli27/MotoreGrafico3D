#version 330 core
out vec4 FragColor;

in vec3 hdrColor;

uniform float exposure;
uniform float gamma;

void main() {
    vec3 mappedColor = hdrColor / (hdrColor + vec3(1.0));
    vec3 finalColor = pow(mappedColor, vec3(1.0 / gamma)) * exposure;
    FragColor = vec4(finalColor, 1.0);
}
