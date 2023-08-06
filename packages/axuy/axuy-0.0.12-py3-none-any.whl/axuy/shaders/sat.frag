#version 330

uniform sampler2D tex;

in vec2 in_text;
out vec4 color;

void main(void)
{
	color = texture(tex, in_text) * 0.69;
	float r = color.r, g = color.g, b = color.b;
	color *= abs(r - g) + abs(g - b) + abs(b - r);
	color -= r * g * b * 4.2;
}
