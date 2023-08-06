#version 330

uniform vec3 color;

in float intensity;
out vec4 color4;

void main()
{
	color4 = vec4(color * intensity, 1.0);
}
