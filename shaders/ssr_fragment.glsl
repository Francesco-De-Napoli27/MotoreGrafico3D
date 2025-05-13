#version 330 core
out vec4 FragColor;

in vec3 fragPos;
in vec3 fragNormal;
in vec3 viewDir;

uniform sampler2D screenTexture;
uniform float maxDistance;
uniform float reflectivity;

void main() {
    // Calcolo della direzione riflessa
    vec3 reflectionDir = reflect(viewDir, fragNormal);

    // Trasforma la direzione riflessa in coordinate dello schermo
    vec2 screenCoords = fragPos.xy + reflectionDir.xy * maxDistance;
    screenCoords = screenCoords * 0.5 + 0.5; // Normalizza a [0,1]

    // Legge il colore della scena nel punto riflesso
    vec3 reflectedColor = texture(screenTexture, screenCoords).rgb;

    // Combina il colore originale con il riflesso
    vec3 finalColor = mix(texture(screenTexture, fragPos.xy).rgb, reflectedColor, reflectivity);
    FragColor = vec4(finalColor, 1.0);
}
