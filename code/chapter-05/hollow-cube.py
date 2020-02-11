# -----------------------------------------------------------------------------
# Python and OpenGL for Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube

vertex = """
uniform mat4   model;         // Model matrix
uniform mat4   view;          // View matrix
uniform mat4   projection;    // Projection matrix
attribute vec4 color;         // Vertex color
attribute vec3 position;      // Vertex position
varying vec3   v_position;    // Interpolated vertex position (out)
varying vec4   v_color;       // Interpolated fragment color (out)
void main()
{
    v_color = color;
    v_position = position;
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
varying vec4 v_color;    // Interpolated fragment color (in)
varying vec3 v_position; // Interpolated vertex position (in)
void main()
{
    float xy = min( abs(v_position.x), abs(v_position.y));
    float xz = min( abs(v_position.x), abs(v_position.z));
    float yz = min( abs(v_position.y), abs(v_position.z));
    float b1 = 0.7;
    float b2 = 0.75;
    float b3 = 0.95;

    if ((xy < b1) && (xz < b1) && (yz < b1))
        discard;
    else if ((xy < b2) && (xz < b2) && (yz < b2))
        gl_FragColor = vec4(0,0,0,1);
    else if ((xy > b3) || (xz > b3) || (yz > b3))
        gl_FragColor = vec4(0,0,0,1);
    else
        gl_FragColor = v_color;
}
"""

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    global phi, theta
    window.clear()

    # Filled cube
    cube.draw(gl.GL_TRIANGLES, I)
    
    # Rotate cube
    theta += 1.0 # degrees
    phi += -1.0 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


V = np.zeros(8, [("position", np.float32, 3),
                 ("color",    np.float32, 4)])
V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                 [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
V["color"]    = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
                 [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]
V = V.view(gloo.VertexBuffer)
I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
              1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
I = I.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(V)

cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)
phi, theta = 40, 30

app.run(framerate=60, framecount=360)
