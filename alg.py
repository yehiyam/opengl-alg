import moderngl
import numpy as np
from PIL import Image
from pyrr import Matrix44
import io
import time
import os

USE_EGL=os.environ.get('USE_EGL', 'True') in ['True', 'true']
if(USE_EGL):
    # -------------------
    # CREATE CONTEXT HERE
    # -------------------
    ctx = moderngl.create_context(
        standalone=True,
        backend='egl',
        headless=True,

    )
else:
    ctx = moderngl.create_context(
        standalone=True,
        libgl='libGL.so.1',
        libx11='libX11.so.6',
        headless=True,
    )

prog = ctx.program(vertex_shader="""
    #version 330
    uniform mat4 model;
    in vec2 in_vert;
    in vec3 in_color;
    out vec3 color;
    void main() {
        gl_Position = model * vec4(in_vert, 0.0, 1.0);
        color = in_color;
    }
    """,
    fragment_shader="""
    #version 330
    in vec3 color;
    out vec4 fragColor;
    void main() {
        fragColor = vec4(color, 1.0);
    }
""")

vertices = np.array([
    -0.6, -0.6,
    1.0, 0.0, 0.0,
    0.6, -0.6,
    0.0, 1.0, 0.0,
    0.0, 0.6,
    0.0, 0.0, 1.0,
], dtype='f4')



def start(args, hkubeApi):
    try:
        input = args.get('input')[0]
        width=input.get('width',512)
        height=input.get('height',512)
        sleep=input.get('sleep',5)
    except Exception as e:
        width=512
        height=512
        sleep=5

    vbo = ctx.buffer(vertices)
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((width, height), 4)])

    fbo.use()
    ctx.clear()
    prog['model'].write(Matrix44.from_eulers((0.0, 0.1, 0.0), dtype='f4'))
    vao.render(moderngl.TRIANGLES)

    data = fbo.read(components=3)
    image = Image.frombytes('RGB', fbo.size, data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    in_mem_file = io.BytesIO()
    image.save(in_mem_file,format='JPEG')
    time.sleep(sleep)
    return {'buffer': in_mem_file.getvalue(), 'size': fbo.size, 'format': 'RGB'}

if __name__ == "__main__":
    with open("1.jpg","wb") as file:
        print('write')
        file.write(start({"input":[{'sleep':0}]}, None).get('buffer'))