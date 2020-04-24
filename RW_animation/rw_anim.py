import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from IPython.display import HTML

# Define parameters for the walk

dims = 1
step_n = 500
step_set = [-1, 0, 1]  # options where to go
origin = np.zeros((1, dims))  # from where to start, creates zeros matrix of dimension corresponding to RW dimension


# Simulate steps in 1D

step_shape = (step_n, dims)
steps = np.random.choice(a=step_set, size=step_shape)  # randomly take Nr.-of-Steps times one direction
path = np.concatenate([origin, steps]).cumsum(0)  # sum how far we got
##put together starting position and then sequence of steps, then apply cumsum over columns
start = path[:1]  # take the first element of the past
stop = path[-1:]  # take the last element of the past

bin_edges = np.arange(min(path), max(path) + 1)


## Set up the figure, the axis, and the plot element we want to animate

fig = plt.figure()
# ax = fig.add_subplot(111, aspect='equal', autoscale_on=False)#, xlim=(-2, 2), ylim=(-2, 2)) #possibility for constant window

# set subplots
ax = fig.add_subplot(121, xlim=(-1, step_n + 1),
                     ylim=(-step_n / 2, step_n / 2))  # (-int(np.sqrt(step_n+1)), int(np.sqrt(step_n+1))))
ax.set_title('Random walk cumulative')

binom_ax = fig.add_subplot(122, ylim=(0, step_n / 2))
binom_ax.set_title('Random walk distribution')

# create our line object which will be modified in the animation,
# here we simply plot an empty line, we'll add data to the line later.
line, = ax.plot([], [], 'o-', lw=2)
# time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes) # we can add time
steps_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
fig.suptitle('1D Random Walk')


# Initialization function: plot the background of each frame

def init():
    """initialize animation"""
    line.set_data([], [])
    # time_text.set_text('')
    steps_text.set_text('')  # to have steps shown on the screen
    return line, steps_text


# Animation function. This is called sequentially, this is the function which is actually plotted

def animate(i):
    x = i  # have steps
    y = path[i]  # get the distance where we are at i-th step
    line.set_data(x, y)  # tuple which will be animated, steps and distance
    # print(x,y)
    # ax.plot(start[:,0], start[:,1],c= 'red', marker='+') #for 2D
    ax.plot(0, start[:, 0], c='red', marker='+')  # to plot starting point as a red cross
    # ax.plot(stop[:,0], stop[:,1],c='black', marker='o') #for 2D
    ax.plot(step_n, stop[:, 0], c='black', marker='o')  # to plot ending point as a black dot
    binom_ax.hist(path[:i], bins=bin_edges, color='b')  # , density = True) # plot the distribution
    # hist, bin_edges = binom_ax.hist(path[:i]) #np.histogram(path, density=True) # this should set bin-edges, does not work

    steps_text.set_text('steps = %i' % i)  # write in the plot the current step
    return line, steps_text


# Plot the whole path and histogram behind the data to make it nicer

# ax.plot(path[:,0], path[:,1],c= 'blue',alpha=0.5,lw=0.25,ls='-'); # for 2D
ax.plot(path[:, 0], c='blue', alpha=0.5, lw=0.25, ls='-');
binom_ax.hist(path[:, 0], bins=bin_edges, color='b', alpha=0.2)  # , density = True)

# Call the animator.  blit=True means only re-draw the parts that have changed.
anim_2plots = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=step_n, interval=100, blit=True)

# Save the animation as an mp4

# This requires ffmpeg or mencoder to be installed.  The extra_args ensure that the x264 codec is used,
# so that the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

anim_2plots.save('RandomWalk_animation_Nsteps_' + str(step_n) + '.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

# Show in a cell for Jupyter, put in a new cell
HTML(anim_2plots.to_html5_video())