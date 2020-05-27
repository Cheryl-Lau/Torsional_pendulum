# -*- coding: utf-8 -*-

import vpython as vp 

# Torsional pendulum snake 

class TorsionalPendulum:
    '''
    For computing rotational pendulum motion of individual rod, with particular 
    mass, length, location on y-axis, and starting angle.
    '''
    def __init__(self, mass, length, y_location, init_theta):
        ''' Create object '''
        self.mass = mass
        self.length = length 
        self.y_location = y_location 

        # Moment of inertia 
        self.inertia = 1/12. * self.mass * self.length**2
        # Initialize angular position theta 
        self.theta = init_theta * vp.pi/180  # convert to radians 
        # Initialize angular velocity omega 
        self.omega = init_omega 

        # Initialize vpython objects 
        self.rod = vp.cylinder(pos=vp.vector(self.length/2.*vp.cos(self.theta),self.y_location,-self.length/2.*vp.sin(self.theta)),
                               axis=vp.vector(-self.length*vp.cos(self.theta),0,self.length*vp.sin(self.theta)),
                               radius=.25,color=vp.color.red)
        self.string = vp.cylinder(pos=vp.vector(0,-10,0),axis=vp.vector(0,y_step*num_rods+10.,0),radius=.1,color=vp.color.white)
        
    def motion(self, dt):
        ''' Rotate rod in SHM '''
        self.dt = dt 
        
        # Update position, omega and alpha
        self.theta += self.omega*dt
        self.alpha = - kappa / self.inertia * self.theta
        self.omega += self.alpha*dt
        
        # Update rod position and axis 
        self.rod.pos = vp.vector(self.length/2.*vp.cos(self.theta),self.y_location,-self.length/2.*vp.sin(self.theta))
        self.rod.axis = vp.vector(-self.length*vp.cos(self.theta),0,self.length*vp.sin(self.theta))
        

''' Input parameters '''

kappa = 8.     
init_theta = 30. # cannot be 0 
init_omega = 0.

num_rods = 200
rod_mass = .2
min_length = 60. 
max_length = 70.

y_step = 1.5
theta_step = 0.1 


''' Set up scene '''

scene = vp.canvas(title='Torsional Pendulum',width=1000,height=700,center=vp.vector(y_step*num_rods/2.,0,0))
#scene.camera.pos = vp.vector(0,y_step*num_rods/2.,5.)
scene.camera.pos = vp.vector(70,-100,20)
scene.camera.axis = vp.vector(-50,100,-20)


''' Create rods '''

def compute_length(y_location):
    # Generate length of ith-rod at y_location, forming a parabolic shape
    # with limits (0,y_step*num_rods), (min_length, max_length)
    y0 = y_step * num_rods  # total length 
    a = (max_length - min_length) / (1/4*y0**2)
    b = -a*y0
    c = max_length
    length = a*y_location**2 + b*y_location + c
    return length 

rod_list = []
y_location = 0.

for i in range(num_rods):
    y_location += y_step
    length = compute_length(y_location)
    init_theta += theta_step
    rod = TorsionalPendulum(rod_mass, length, y_location, init_theta)
    rod_list.append(rod)
    

''' Animation '''

dt = 0.01

while True:
    vp.rate(5000000000)
    for rod in rod_list:
        rod.motion(dt)





















