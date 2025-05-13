#version 330 core
out vec4 FragColor;

in vec3 fragPos;
in vec3 fragNormal;

uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 viewPos;
uniform float bounceFactor;

void main() {
    // Normale e direzione della luce
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPos);

    // Illuminazione diretta
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Illuminazione indiretta (Global Illumination)
    vec3 indirectLight = diffuse * bounceFactor;

    vec3 result = diffuse + indirectLight;
    FragColor = vec4(result, 1.0);
}
