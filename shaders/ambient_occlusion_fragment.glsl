#version 330 core
out vec4 FragColor;

in vec3 fragPos;
in vec3 fragNormal;

uniform float intensity;
uniform float radius;
uniform int samples;
uniform sampler2D noiseTexture;

void main() {
    // Calcolo del fattore di occlusione
    float occlusion = 0.0;
    for (int i = 0; i < samples; i++) {
        vec3 samplePos = fragPos + fragNormal * radius * texture(noiseTexture, fragPos.xy).r;
        float influence = max(0.0, dot(fragNormal, normalize(samplePos - fragPos)));
        occlusion += influence;
    }

    occlusion = 1.0 - (occlusion / float(samples) * intensity);

    vec3 finalColor = vec3(occlusion);  // Oscuramento sulle aree occluse
    FragColor = vec4(finalColor, 1.0);
}
