#version 330

uniform vec3 camera;
uniform sampler2D tex;
uniform sampler2D norm;

/* Enumerates */
const uint FACEX = 0u;
const uint FACEY = 1u;
const uint FACEZ = 2u;

/* Matrices rotates Oz vector to Ox and Oy */
const mat3 ROTX = mat3(0, 0, 1, 0, 1, 0, -1, 0, 0);
const mat3 ROTY = mat3(1, 0, 0, 0, 0, -1, 0, 1, 0);

in vec3 tex_vert;
in vec3 color;
out vec4 color4;

void main()
{
	/* Map vertices are whole numbers. */
	uint face;
	if (fract(tex_vert.x) == 0)
		face = FACEX;
	else if (fract(tex_vert.y) == 0)
		face = FACEY;
	else
		face = FACEZ;

	vec2 tex_vert2;
	if (face == FACEX)
		tex_vert2 = vec2(tex_vert.y, tex_vert.z);
	else if (face == FACEY)
		tex_vert2 = vec2(tex_vert.z, tex_vert.x);
	else
		tex_vert2 = vec2(tex_vert.x, tex_vert.y);

	vec3 normal = normalize(texture(norm, tex_vert2) * 2.0 - 1.0).xyz;
	/* Odd matmul order, but we take absolute value of the dot product. */
	if (face == FACEX)
		normal *= ROTX;
	else if (face == FACEY)
		normal *= ROTY;
	float diffuse = abs(dot(normal, normalize(camera - tex_vert)));
	color4 = diffuse * vec4(color, 1.0) * texture(tex, tex_vert2);
}
