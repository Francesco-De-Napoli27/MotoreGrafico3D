#version 330 core
out vec4 FragColor;

in vec3 fragPos;
uniform float focalDistance;
uniform float blurFactor;
uniform sampler2D screenTexture;

void main() {
    float depth = abs(focalDistance - fragPos.z);
    float blurAmount = depth * blurFactor;

    vec3 color = texture(screenTexture, fragPos.xy).rgb;
    for (int i = -2; i <= 2; i++) {
        color += texture(screenTexture, fragPos.xy + vec2(float(i)) * blurAmount).rgb;
    }
    color /= 6.0;

    FragColor = vec4(color, 1.0);
}
