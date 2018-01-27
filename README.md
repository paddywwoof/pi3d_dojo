**pi3d_dojo**

A DIY 3D platform game for messing about with and, hopefully, learning
a little bit about 3D graphics, python and programming generally.

`platform01.py` was the starting point and `platform02.py` the evolution
after a couple of hours tweaking (at Bradford CoderDojo 27 Jan 2018). Hack
away - remember you can't break anything. Well, you can always restore
these versions from github!

You need to have python running and install a few libraries. On the Raspberry
Pi raspbian everything is there apart from pi3d so just:

    $ pip3 install pi3d
    $ git clone https://github/paddywwoof/pi3d_dojo.git
    $ cd pi3d_dojo
    $ python3 platform01.py


On linux you will need mesa-utils-extra On windows you need to install some
DLLs that emulate OpenGLES2.0 behaviour (equivalent of mesa). See instructions
here http://http://pi3d.github.io/ under ReadMe for installation
and general help.

There are lots of demos available https://github.com/pi3d/pi3d_demos
