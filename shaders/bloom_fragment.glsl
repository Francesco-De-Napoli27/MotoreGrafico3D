#version 330 core
out vec4 FragColor;

in vec3 fragColor;
uniform float blurStrength;

void main() {
    vec3 blurredColor = fragColor * blurStrength;
    FragColor = vec4(blurredColor, 1.0);
}
