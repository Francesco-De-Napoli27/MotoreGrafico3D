#version 330 core
out vec4 FragColor;

in vec3 fragPos;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform float density;

void main() {
    // Calcolo dello scattering atmosferico
    float distance = length(lightPos - fragPos);
    float scattering = exp(-density * distance);

    vec3 finalColor = lightColor * scattering;
    FragColor = vec4(finalColor, 1.0);
}
