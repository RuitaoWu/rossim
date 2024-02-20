# coding: utf-8
#
#  Copyright (C) 2008-2010 Istituto per l'Interscambio Scientifico I.S.I.
#  You can contact us by email (isi@isi.it) or write to:
#  ISI Foundation, Viale S. Severo 65, 10133 Torino, Italy. 
#
#  This program was written by André Panisson <panisson@gmail.com>
#  https://github.com/panisson/pymobility/tree/master
#  git://github.com/panisson/pymobility.git
'''
Created on Jan 24, 2012

@author: André Panisson
@contact: panisson@gmail.com
@organization: ISI Foundation, Torino, Italy
'''
import numpy as np
from numpy.random import rand

# define a Uniform Distribution
U = lambda MIN, MAX, SAMPLES: rand(*SAMPLES.shape) * (MAX - MIN) + MIN

# define a Truncated Power Law Distribution
P = lambda ALPHA, MIN, MAX, SAMPLES: ((MAX ** (ALPHA+1.) - 1.) * rand(*SAMPLES.shape) + 1.) ** (1./(ALPHA+1.))

# define an Exponential Distribution
E = lambda SCALE, SAMPLES: -SCALE*np.log(rand(*SAMPLES.shape))

# *************** Palm state probability **********************
def pause_probability_init(pause_low, pause_high, speed_low, speed_high, dimensions):
    alpha1 = ((pause_high+pause_low)*(speed_high-speed_low))/(2*np.log(speed_high/speed_low))
    delta1 = np.sqrt(np.sum(np.square(dimensions)))
    return alpha1/(alpha1+delta1)

# *************** Palm residual ******************************
def residual_time(mean, delta, shape=(1,)):
    t1 = mean - delta;
    t2 = mean + delta;
    u = rand(*shape);
    residual = np.zeros(shape)
    if delta != 0.0:
        case_1_u = u < (2.*t1/(t1+t2))
        residual[case_1_u] = u[case_1_u]*(t1+t2)/2.
        residual[np.logical_not(case_1_u)] = t2-np.sqrt((1.-u[np.logical_not(case_1_u)])*(t2*t2 - t1*t1))
    else:
        residual=u*mean  
    return residual

# *********** Initial speed ***************************
def initial_speed(speed_mean, speed_delta, shape=(1,)):
    v0 = speed_mean - speed_delta
    v1 = speed_mean + speed_delta
    u = rand(*shape)
    return pow(v1, u) / pow(v0, u - 1)

def init_random_waypoint(nr_nodes, dimensions,
                         speed_low, speed_high, pause_low, pause_high):

    ndim = len(dimensions)
    positions = np.empty((nr_nodes, ndim))
    waypoints = np.empty((nr_nodes, ndim))
    speed = np.empty(nr_nodes)
    pause_time = np.empty(nr_nodes)

    speed_low = float(speed_low)
    speed_high = float(speed_high)

    moving = np.ones(nr_nodes)
    speed_mean, speed_delta = (speed_low+speed_high)/2., (speed_high-speed_low)/2.
    pause_mean, pause_delta = (pause_low+pause_high)/2., (pause_high-pause_low)/2.

    # steady-state pause probability for Random Waypoint
    q0 = pause_probability_init(pause_low, pause_high, speed_low, speed_high, dimensions)
    
    for i in range(nr_nodes):
        
        while True:

            z1 = rand(ndim) * np.array(dimensions)
            z2 = rand(ndim) * np.array(dimensions)

            if rand() < q0:
                moving[i] = 0.
                break
            else:
                #r is a ratio of the length of the randomly chosen path over
                # the length of a diagonal across the simulation area
                r = np.sqrt(np.sum((z2 - z1) ** 2) / np.sum(np.array(dimensions) ** 2))
                if rand() < r:
                    moving[i] = 1.
                    break

        positions[i] = z1
        waypoints[i] = z2

    # steady-state positions
    # initially the node has traveled a proportion u2 of the path from (x1,y1) to (x2,y2)
    u2 = rand(*positions.shape)
    positions = u2*positions + (1 - u2)*waypoints

    # steady-state speed and pause time
    paused_bool = moving==0.
    paused_idx = np.where(paused_bool)[0]
    pause_time[paused_idx] = residual_time(pause_mean, pause_delta, paused_idx.shape)
    speed[paused_idx] = 0.0

    moving_bool = np.logical_not(paused_bool)
    moving_idx = np.where(moving_bool)[0]
    pause_time[moving_idx] = 0.0
    speed[moving_idx] = initial_speed(speed_mean,speed_delta, moving_idx.shape)

    return positions, waypoints, speed, pause_time

class RandomWaypoint(object):
    
    def __init__(self, nr_nodes, dimensions, velocity=(0.1, 1.), wt_max=None):
        '''
        Random Waypoint model.
        
        Required arguments:
        
          *nr_nodes*:
            Integer, the number of nodes.
          
          *dimensions*:
            Tuple of Integers, the x and y dimensions of the simulation area.
          
        keyword arguments:
        
          *velocity*:
            Tuple of Integers, the minimum and maximum values for node velocity.
          
          *wt_max*:
            Integer, the maximum wait time for node pauses.
            If wt_max is 0 or None, there is no pause time.
        '''
        
        self.nr_nodes = nr_nodes
        self.dimensions = dimensions
        self.velocity = velocity
        self.wt_max = wt_max
        self.init_stationary = True
    
    def __iter__(self):
        
        ndim = len(self.dimensions)
        MIN_V, MAX_V = self.velocity
        
        wt_min = 0.
        
        if self.init_stationary:

            positions, waypoints, velocity, wt = \
                init_random_waypoint(self.nr_nodes, self.dimensions, MIN_V, MAX_V, wt_min, 
                             (self.wt_max if self.wt_max is not None else 0.))
        else:

            NODES = np.arange(self.nr_nodes)
            positions = U(np.zeros(ndim), np.array(self.dimensions), np.dstack((NODES,)*ndim)[0])
            waypoints = U(np.zeros(ndim), np.array(self.dimensions), np.dstack((NODES,)*ndim)[0])
            wt = np.zeros(self.nr_nodes)
            velocity = U(MIN_V, MAX_V, NODES)

        # assign nodes' movements (direction * node velocity)
        direction = waypoints - positions
        direction /= np.linalg.norm(direction, axis=1)[:, np.newaxis]
        
        while True:
            # update node position
            positions += direction * velocity[:, np.newaxis]
            # calculate distance to waypoint
            d = np.sqrt(np.sum(np.square(waypoints - positions), axis=1))
            # update info for arrived nodes
            arrived = np.where(np.logical_and(d<=velocity, wt<=0.))[0]
            
            # step back for nodes that surpassed waypoint
            positions[arrived] = waypoints[arrived]
            
            if self.wt_max:
                velocity[arrived] = 0.
                wt[arrived] = U(0, self.wt_max, arrived)
                # update info for paused nodes
                wt[np.where(velocity==0.)[0]] -= 1.
                # update info for moving nodes
                arrived = np.where(np.logical_and(velocity==0., wt<0.))[0]
            
            if arrived.size > 0:
                waypoints[arrived] = U(np.zeros(ndim), np.array(self.dimensions), np.zeros((arrived.size, ndim)))
                velocity[arrived] = U(MIN_V, MAX_V, arrived)

                new_direction = waypoints[arrived] - positions[arrived]
                direction[arrived] = new_direction / np.linalg.norm(new_direction, axis=1)[:, np.newaxis]
            
            self.velocity = velocity
            self.wt = wt
            yield positions

class StochasticWalk(object):
    
    def __init__(self, nr_nodes, dimensions, FL_DISTR, VELOCITY_DISTR, WT_DISTR=None, border_policy='reflect'):
        '''
        Base implementation for models with direction uniformly chosen from [0,pi]:
        random_direction, random_walk, truncated_levy_walk
        
        Required arguments:
        
          *nr_nodes*:
            Integer, the number of nodes.
          
          *dimensions*:
            Tuple of Integers, the x and y dimensions of the simulation area.
            
          *FL_DISTR*:
            A function that, given a set of samples, 
             returns another set with the same size of the input set.
            This function should implement the distribution of flight lengths
             to be used in the model.
             
          *VELOCITY_DISTR*:
            A function that, given a set of flight lengths, 
             returns another set with the same size of the input set.
            This function should implement the distribution of velocities
             to be used in the model, as random or as a function of the flight lengths.
          
        keyword arguments:
        
          *WT_DISTR*:
            A function that, given a set of samples, 
             returns another set with the same size of the input set.
            This function should implement the distribution of wait times
             to be used in the node pause.
            If WT_DISTR is 0 or None, there is no pause time.
            
          *border_policy*:
            String, either 'reflect' or 'wrap'. The policy that is used when the node arrives to the border.
            If 'reflect', the node reflects off the border.
            If 'wrap', the node reappears at the opposite edge (as in a torus-shaped area).
        '''
        self.collect_fl_stats = False
        self.collect_wt_stats = False
        self.border_policy = border_policy
        self.dimensions = dimensions
        self.nr_nodes = nr_nodes
        self.FL_DISTR = FL_DISTR
        self.VELOCITY_DISTR = VELOCITY_DISTR
        self.WT_DISTR = WT_DISTR
        
    def __iter__(self):
        def reflect(xy):
            # node bounces on the margins
            for dim, max_d in enumerate(self.dimensions):
                b = np.where(xy[:,dim]<0)[0]
                if b.size > 0:
                    xy[b,dim] = - xy[b,dim]
                    movement[b,dim] = -movement[b,dim]
                b = np.where(xy[:,dim]>max_d)[0]
                if b.size > 0:
                    xy[b,dim] = 2*max_d - xy[b,dim]
                    movement[b,dim] = -movement[b,dim]
        
        def wrap(xy):
            for dim, max_d in enumerate(self.dimensions):
                b = np.where(xy[:,dim]<0)[0]
                if b.size > 0: xy[b,dim] += max_d
                b = np.where(xy[:,dim]>max_d)[0]
                if b.size > 0: xy[b,dim] -= max_d
        
        if self.border_policy == 'reflect':
            borderp = reflect
        elif self.border_policy == 'wrap':
            borderp = wrap
        else:
            borderp = self.border_policy
        
        ndim = len(self.dimensions)
        NODES = np.arange(self.nr_nodes)

        # assign node's positions, flight lengths and velocities
        xy = U(np.zeros(ndim), np.array(self.dimensions), np.dstack((NODES,)*ndim)[0])
        fl = self.FL_DISTR(NODES)
        velocity = self.VELOCITY_DISTR(fl)

        # assign nodes' movements (direction * node velocity)
        direction = U(0., 1., np.zeros((self.nr_nodes, ndim))) - 0.5
        direction /= np.linalg.norm(direction, axis=1)[:, np.newaxis]
        movement = direction * velocity[:, np.newaxis]

        # starts with no wating time
        wt = np.zeros(self.nr_nodes)
        
        if self.collect_fl_stats: self.fl_stats = list(fl)
        if  self.collect_wt_stats: self.wt_stats = list(wt)

        while True:
    
            xy += movement
            fl -= velocity
            
            # step back for nodes that surpassed fl
            arrived = np.where(np.logical_and(velocity>0., fl<=0.))[0]
            if arrived.size > 0:
                diff = fl.take(arrived) / velocity.take(arrived)
                xy[arrived] += np.dstack((diff,)*ndim)[0] * movement[arrived]
            
            # apply border policy
            borderp(xy)
            
            if self.WT_DISTR:
                velocity[arrived] = 0.
                wt[arrived] = self.WT_DISTR(arrived)
                if self.collect_wt_stats: self.wt_stats.extend(wt[arrived])
                # update info for paused nodes
                wt[np.where(velocity==0.)[0]] -= 1.
                arrived = np.where(np.logical_and(velocity==0., wt<0.))[0]
            
            # update info for moving nodes
            if arrived.size > 0:
                
                fl[arrived] = self.FL_DISTR(arrived)
                if self.collect_fl_stats: self.fl_stats.extend(fl[arrived])
                velocity[arrived] = self.VELOCITY_DISTR(fl[arrived])
                v = velocity[arrived]
                direction = U(0., 1., np.zeros((arrived.size, ndim))) - 0.5
                direction /= np.linalg.norm(direction, axis=1)[:, np.newaxis]
                movement[arrived] = v[:, np.newaxis] * direction
    
            yield xy

class RandomWalk(StochasticWalk):
    
    def __init__(self, nr_nodes, dimensions, velocity=1., distance=1., border_policy='reflect'):
        '''
        Random Walk mobility model.
        This model is based in the Stochastic Walk, but both the flight length and node velocity distributions are in fact constants,
        set to the *distance* and *velocity* parameters. The waiting time is set to None.
        
        Required arguments:
        
          *nr_nodes*:
            Integer, the number of nodes.
          
          *dimensions*:
            Tuple of Integers, the x and y dimensions of the simulation area.
          
        keyword arguments:
        
          *velocity*:
            Double, the value for the constant node velocity. Default is 1.0
          
          *distance*:
            Double, the value for the constant distance traveled in each step. Default is 1.0
            
          *border_policy*:
            String, either 'reflect' or 'wrap'. The policy that is used when the node arrives to the border.
            If 'reflect', the node reflects off the border.
            If 'wrap', the node reappears at the opposite edge (as in a torus-shaped area).
        '''
        if velocity>distance:
            # In this implementation, each step is 1 second,
            # it is not possible to have a velocity larger than the distance
            raise Exception('Velocity must be <= Distance')
        
        fl = np.zeros(nr_nodes)+distance
        vel = np.zeros(nr_nodes)+velocity
        
        FL_DISTR = lambda SAMPLES: np.array(fl[:len(SAMPLES)])
        VELOCITY_DISTR = lambda FD: np.array(vel[:len(FD)])
        
        StochasticWalk.__init__(self, nr_nodes, dimensions, FL_DISTR, VELOCITY_DISTR,border_policy=border_policy)

class RandomDirection(StochasticWalk):
    
    def __init__(self, nr_nodes, dimensions, wt_max=None, velocity=(0.1, 1.), border_policy='reflect'):
        '''
        Random Direction mobility model.
        This model is based in the Stochastic Walk. The flight length is chosen from a uniform distribution, 
        with minimum 0 and maximum set to the maximum dimension value.
        The velocity is also chosen from a uniform distribution, with boundaries set by the *velocity* parameter.
        If wt_max is set, the waiting time is chosen from a uniform distribution with values between 0 and wt_max.
        If wt_max is not set, waiting time is set to None.
        
        Required arguments:
        
          *nr_nodes*:
            Integer, the number of nodes.
          
          *dimensions*:
            Tuple of Integers, the x and y dimensions of the simulation area.
          
        keyword arguments:
        
          *wt_max*:
            Double, maximum value for the waiting time distribution.
            If wt_max is set, the waiting time is chosen from a uniform distribution with values between 0 and wt_max.
            If wt_max is not set, the waiting time is set to None.
            Default is None.
          
          *velocity*:
            Tuple of Doubles, the minimum and maximum values for node velocity.
            
          *border_policy*:
            String, either 'reflect' or 'wrap'. The policy that is used when the node arrives to the border.
            If 'reflect', the node reflects off the border.
            If 'wrap', the node reappears at the opposite edge (as in a torus-shaped area).
        '''
        
        MIN_V, MAX_V = velocity
        FL_MAX = max(dimensions)
        
        FL_DISTR = lambda SAMPLES: U(0, FL_MAX, SAMPLES)
        if wt_max:
            WT_DISTR = lambda SAMPLES: U(0, wt_max, SAMPLES)
        else:
            WT_DISTR = None
        VELOCITY_DISTR = lambda FD: U(MIN_V, MAX_V, FD)
        
        StochasticWalk.__init__(self, nr_nodes, dimensions, FL_DISTR, VELOCITY_DISTR, WT_DISTR=WT_DISTR, border_policy=border_policy)

        
def random_waypoint(*args, **kwargs):
    return iter(RandomWaypoint(*args, **kwargs))

def stochastic_walk(*args, **kwargs):
    return iter(StochasticWalk(*args, **kwargs))

def random_walk(*args, **kwargs):
    return iter(RandomWalk(*args, **kwargs))

def random_direction(*args, **kwargs):
    return iter(RandomDirection(*args, **kwargs))
