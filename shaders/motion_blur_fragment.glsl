#version 330 core
out vec4 FragColor;

in vec3 fragPos;
uniform sampler2D screenTexture;
uniform vec2 blurDirection;
uniform float blurStrength;

void main() {
    vec3 color = vec3(0.0);
    for (int i = -2; i <= 2; i++) {
        color += texture(screenTexture, fragPos.xy + blurDirection * blurStrength * float(i)).rgb;
    }
    color /= 5.0;  // Media per ottenere il blur morbido

    FragColor = vec4(color, 1.0);
}
