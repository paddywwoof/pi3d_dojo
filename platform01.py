#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import math,random
import time
import pi3d

## Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=50, y=50,  frames_per_second=20)

# load shaders
shader = pi3d.Shader("uv_bump")
flatsh = pi3d.Shader("uv_flat")

# load textures
metlimg = pi3d.Texture("metalhull.jpg")
plntimg = pi3d.Texture("planet10.jpg")
mudnorm = pi3d.Texture("mudnormal.jpg")
flrnorm = pi3d.Texture("floor_nm.jpg")
grsnorm = pi3d.Texture("grasstile_n.jpg")
ectex = pi3d.Texture('skybox_interstellar.jpg')

FOG = ((0.3, 0.3, 0.4, 0.8), 350.0) # distant hills look distant

myecube = pi3d.EnvironmentCube(size=900.0, maptype='CROSS')
myecube.set_draw_details(flatsh, [ectex])

# Create elevation map
mapsize = 900.0
mapheight = 150.0
mymap = pi3d.ElevationMap("mars_height.png", name="map",
                     width=mapsize, depth=mapsize, height=mapheight,
                     divx=32, divy=32) 
mymap.set_draw_details(shader, [plntimg, mudnorm], 128.0, 0.0)
mymap.set_fog(*FOG)

# ball stuff
DRAG = 0.02                          # 2% reduction in speed each frame
G = -0.01                            # g -> change in y velocity each frame
rot = 0.0                            # rotation of camera about vertical axis
ballrot = 180.0                      # heading of ball about vert axis (y)
tilt = 0.0                           # rotation of camera about local x axis (left to right horizontal)
RADIUS = 1.0                         # radius of ball
ball = pi3d.Triangle(corners=((-0.01, 0.0), (0.0, 0.01), (0.01, 0.0))) # an 'empty' game object
ball_shape = pi3d.Sphere(radius=RADIUS, slices=24, sides=24) # the visible shape
ball.add_child(ball_shape)           # to get realistic 'rolling'
ball_shape.set_draw_details(shader, [plntimg, flrnorm], 4.0)

# platforms
W = 8.0
H = 1.5
on_plat = False                      # flag if on a platform (for jumping)
platforms = [                        # locations of platforms
  pi3d.Cuboid(x=44, y=5, z=43),
  pi3d.Cuboid(x=32, y=3, z=28),
  pi3d.Cuboid(x=30, y=2, z=15),
  pi3d.Cuboid(x=15, y=1, z=5),
  pi3d.Cuboid(x=0, y=2, z=0),
  ]

for p in platforms:
  p.scale(W, H, W)
  p.set_draw_details(shader, [metlimg, flrnorm], 8.0)
  p.positionY(p.y() + mymap.calcHeight(p.x(), p.z())) # adjust for terrain

dr = 0.0                             # rolling speed
dy = 0.0                             # vertical speed (for jumping)
expl = 1.0                           # scale value for exploding
xb, yb, zb = platforms[0].x(), platforms[0].y() + RADIUS + 5.0, platforms[0].z()
                                     # ball location coordinates
xc, yc, zc = xb, yb, zb              # set camera coords equal to ball coords

# end pole
xp, zp = 0.0, 0.0
yp = mymap.calcHeight(xp, zp) + 5
pole = pi3d.Cone(radius=0.5, height=10, x=xp, y=yp, z=zp)
pole.set_draw_details(shader, [metlimg, flrnorm], 12.0)

# keyboard object for getting key presses
mykeys = pi3d.Keyboard()
# mouse for steering
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()

CAMERA = pi3d.Camera()
# main game loop
while DISPLAY.loop_running():
  mx, my = mymouse.position()
  rot = -mx * 0.2
  tilt = my * 0.1 -10.0
  if tilt > 5.0:
    tilt = 5.0
  sf = 5.0 - 2.5 / abs(tilt) if tilt < -1.0 else 2.5
  xc += (xb - xc) * 0.05
  yc += (yb - yc) * 0.05
  zc += (zb - zc) * 0.05
  CAMERA.relocate(rot, tilt, [xc, yc + 1.0, zc], [-sf, -sf, -sf])
  ballrot +=  ((rot - ballrot) % 360 - 180) * 0.05
  dr *= 1.0 - DRAG
  xb -= dr * math.sin(math.radians(ballrot))
  zb += dr * math.cos(math.radians(ballrot))
  dy += G # has -ve value so increase downward velocity
  yb += dy # position changes by velocity

  # check position
  if abs(xp - xb) < RADIUS and abs(zp - zb) < RADIUS:
    pole.set_material((1.0, 0.0, 0.0))

  on_plat = False
  for p in platforms:
    px, py, pz = p.x(), p.y(), p.z() # convience variables to save multiple func calls
    roll_ht = py + RADIUS + H * 0.5
    if (abs(xb - px) < (W * 0.5) and abs(zb - pz) < (W * 0.5) and
        yb < roll_ht and yb > (roll_ht - RADIUS)): # on a platform
      yb = roll_ht
      dy = 0
      on_plat = True
      break # shouldn't be on more than one platform at once!

  ht = mymap.calcHeight(xb, zb)
  if yb < (ht + RADIUS):                   # this is on the ground - explode!
    yb = ht + RADIUS
    dy = 0
    ball.scale(expl, expl, expl)
    expl *= 1.25                           # increase size 25% each frame
    ball_shape.set_material((0.2 * expl, 0.0, 0.0))
    if expl > 10.0:
      dr = 0.0                             # rolling speed
      dy = 0.0                             # vertical speed (for jumping)
      expl = 1.0                           # scale value for exploding
      ball_shape.set_material((0.5, 0.5, 0.5))
      ball.scale(expl, expl, expl)
      xb, yb, zb = platforms[0].x(), platforms[0].y() + RADIUS + 5.0, platforms[0].z()
                                           # ball location coordinates
      xc, yc, zc = xb, yb, zb              # set camera coords equal to ball coords
  ball.position(xb, yb, zb)
  ball.rotateToY(-ballrot)
  ball_shape.rotateIncX(dr * 50)
  ball.draw()
  pole.draw()
  for p in platforms:
    p.draw()
  mymap.draw()
  mymap.position(0.0, 0.0, 0.0)
  myecube.draw()

  k = mykeys.read()
  if k >-1:
    if k == ord('w') or  k == 259 or k == 134:  #forward boost w or up key
      dr -= 0.1
    elif k == ord('s') or  k == 258 or k == 135:  #backward boost s or down key
      dr += 0.1
    elif k == ord(' ') and on_plat:   #key SPACE
      dy += 0.3
    elif k == 27:  #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.stop()
      break
