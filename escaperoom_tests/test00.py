import sys
sys.path.insert(1,'/home/pi/pi3d') # to use local 'develop' branch version
import pi3d
import numpy as np

RANGE = 100.0
MODEL_PATH = '{}'
display = pi3d.Display.create(background=(0.0, 0.0, 0.0, 0.0))
shader = pi3d.Shader('uv_light')
laser_shader = pi3d.Shader('mat_flat')

# pod and laser
pod = pi3d.Model(file_string=MODEL_PATH.format('pod_2.obj'), z=20.0)
laser_base = pi3d.Model(file_string=MODEL_PATH.format('laser_base_2.obj'), y=3.15)
laser_gun = pi3d.Model(file_string=MODEL_PATH.format('laser_gun_2.obj'), y=0.4, z=-0.4)
laser_tip = pi3d.Cylinder(radius=0.05, height=5.0, rx=90.0, y=0.28)
laser_tip.set_material((1.0, 0.0, 0.0))
laser_tip.set_alpha(0.0)
laser_gun.add_child(laser_tip)
laser_base.add_child(laser_gun)
pod.add_child(laser_base)
pod.set_shader(shader) # all use uv_light shader
laser_tip.set_shader(laser_shader)

# asteroid
asteroid = pi3d.Model(file_string=MODEL_PATH.format('asteroid_large_1.obj'), z=50, y=10, x=20)
asteroid.set_shader(shader)

keys = pi3d.Keyboard()
mouse = pi3d.Mouse(restrict=False)
mouse.start()

blast_dist = 0.0

while display.loop_running():
  pod.draw()
  asteroid.draw()
  asteroid.rotateIncX(1.5)
  asteroid.rotateIncZ(2.0)
  mx, my = mouse.position()
  laser_base.rotateToY(mx)
  laser_gun.rotateToX(max(min(20, -my), -85))
  if blast_dist > 0.0:
    laser_tip.set_alpha(0.8)
    laser_tip.positionZ(2.5 + blast_dist)
    blast_dist += 5.0
    if blast_dist > RANGE:
      blast_dist = 0.0
      laser_tip.set_alpha(0.0)
  k = keys.read()
  if k >-1:
    if k == ord('a'):
      pod.translateX(-0.1)
    elif k == ord('d'):
      pod.translateX(0.1)
    elif k == ord('w'):
      pod.translateY(0.1)
    elif k == ord('s'):
      pod.translateY(-0.1)
    elif k == ord('z'):
      pod.translateZ(0.1)
    elif k == ord('x'):
      pod.translateZ(-0.1)
    elif k == ord('j'):
      pod.rotateIncY(2)
    elif k == ord('l'):
      pod.rotateIncY(-2)
    elif k == ord('i'):
      pod.rotateIncX(2)
    elif k == ord('k'):
      pod.rotateIncX(-2)
    elif k == ord(' '): # shoot with space
      blast_dist = 0.5 # positive value 'sets it off'
      ''' hit test check direction of pulse '''
      but_pt, aim_vec = laser_gun.transform_direction([0.0, 0.0, 1.0])
      dir_vec = asteroid.unif[0:3] - but_pt # vector to asteroid
      # dir_vec = asteroid.xyz - but_pt # can do this after pi3d v2.21
      len_dir = np.dot(dir_vec, dir_vec) ** 0.5 # std length calc
      if len_dir > 0: # just in case laser and asteroid are in same place!
        dir_vec /= len_dir # normalise
        c_prod = np.cross(dir_vec, aim_vec) # cross product of two vectors
        sin_ang = np.dot(c_prod, c_prod) ** 0.5 # magnitude of cross product is sin angle between as both unit vecs
        print(sin_ang, c_prod)
    elif k==27:
      keys.close()
      display.destroy()
      break
