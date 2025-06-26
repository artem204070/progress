
        #version 330 core

        in vec3 frag_pos;
        in vec3 frag_normal;
        in vec2 frag_texcoord;

        out vec4 out_color;

        uniform sampler2D texture0;

        void main() {
            vec4 tex_color = texture(texture0, frag_texcoord);
            if (tex_color.a < 0.1) discard;

            // Простое освещение
            vec3 light_dir = normalize(vec3(1.0, 1.0, 1.0));
            float diff = max(dot(normalize(frag_normal), light_dir), 0.2);

            out_color = tex_color * vec4(vec3(diff), 1.0);
        }
        