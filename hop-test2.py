#!/usr/bin/python
# Implements the stochastic Hopf-bifurcation model illustrated in
# Week 308 of John Baez's This Week's Finds
# http://johncarlosbaez.wordpress.com/2010/12/24/this-weeks-finds-week-308/

import sys, random  # Python ships with these
import scipy, pylab  # these are extra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


def alpha(t):
    return 0.1


def beta(t):
    return 0.1


def hopf(x, y, gamma, dt, lamb):
    """
    Compute the change in coordinates given the current position,
    the parameters which govern the stochastic Hopf dynamics and the 
    Euler integration timestep.
    """
    a = alpha(dt)
    b = beta(dt)

    dx = y * dt
    dy = -a * (gamma ** 2) - b * (
    gamma ** 2) * x - gamma ** 2 * x ** 3 - gamma * x ** 2 * y + gamma ** 2 * x ** 2 - gamma * x * y * dt
    if lamb != 0.0:
        sigma = sqrt(dt)
        dx += lamb * gauss(mu=0.0, sigma=sigma)
        dy += lamb * gauss(mu=0.0, sigma=sigma)
    return dx, dy


gamma = 4  # amplitude / x-y correlation
lamb = 0.00001  # noise strength
dt = 0.01  # timestep
x_init = 0.0  # initial value for x
y_init = 0.0  # initial value for y
T = int(1e2)  # duration of the simulation
animation_speed = 0.001

# pull functions out of libraries for our later convenience
gauss = random.gauss
sqrt = scipy.sqrt


# initialize the arrays of coordinate values
aX = scipy.zeros(T)
aY = scipy.zeros(T)
aX[0] = x_init
aY[0] = y_init

# MAIN LOOP
print "starting calc"
for time_step in xrange(1, T):
    x = aX[time_step - 1]
    y = aY[time_step - 1]
    dx, dy = hopf(x, y, gamma, dt, lamb)
    aX[time_step] = x + dx
    aY[time_step] = y + dy
    lamb = 0.0
    percent_done = float(time_step) / T * 100
    if percent_done % 10 == 0:
        print str(percent_done) + "%"
print "calc finished"
aX = aX[1:]
aY = aY[1:]

# display output
# Fig. 1: X vs. Y
pylab.plot(aX, aY)
pylab.xlabel("X")
pylab.ylabel("Y")
pylab.title("gamma = " + str(gamma)
            + ", lambda = " + str(lamb))


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(min(aX), max(aX)), ylim=(min(aY), max(aY)))
# ax = plt.axes(xlim=(-10,10), ylim=(-10, 10))
line, = ax.plot([], [], lw=2)


# initialization function: plot the background of each frame
def init():
    line.set_data([aX[0]], [aX[0]])
    return line,


# animation function.  This is called sequentially
def animate(i):
    if animation_speed > 1:
        x = aX[:i * animation_speed]
        y = aY[:i * animation_speed]
    else:
        x = aX[:i]
        y = aY[:i]
    # xHist.append(x)
    # yHist.append(y)
    line.set_data(x, y)
    # print x, y
    return line,


# call the animator.  blit=True means only re-draw the parts that have changed.
if animation_speed < 1:
    interval = animation_speed
else:
    interval = 1
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(aX), interval=interval, blit=True)


# Fig. 2: X as a function of time
pylab.figure()
pylab.plot(aX)
pylab.xlabel("Time")
pylab.ylabel("X")
pylab.title("gamma = " + str(gamma)
            + ", lambda = " + str(lamb))
pylab.show()
