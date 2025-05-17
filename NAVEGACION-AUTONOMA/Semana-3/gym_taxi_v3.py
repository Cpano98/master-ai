import gym
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def run_animation(experience_buffer):
    """Function to run animation"""
    time_lag = 0.05  # Delay (in s) between frames
    for experience in experience_buffer:
        # Plot frame
        clear_output(wait=True)
        plt.imshow(experience['frame'])
        plt.axis('off')
        plt.show()

        # Print console output
        print(f"Episode: {experience['episode']}/{experience_buffer[-1]['episode']}")
        print(f"Epoch: {experience['epoch']}/{experience_buffer[-1]['epoch']}")
        print(f"State: {experience['state']}")
        print(f"Action: {experience['action']}")
        print(f"Reward: {experience['reward']}")
        # Pauze animation
        sleep(time_lag)
        
def store_episode_as_gif(experience_buffer, path='./', filename='animation.gif'):
    """Store episode as gif animation"""
    fps = 5   # Set framew per seconds
    dpi = 300  # Set dots per inch
    interval = 50  # Interval between frames (in ms)

    # Retrieve frames from experience buffer
    frames = []
    for experience in experience_buffer:
        frames.append(experience['frame'])

    # Fix frame size
    plt.figure(figsize=(frames[0].shape[1] / dpi, frames[0].shape[0] / dpi), dpi=dpi)
    patch = plt.imshow(frames[0])
    plt.axis('off')

    # Generate animation
    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=interval)

    # Save output as gif
    anim.save(path + filename, writer='imagemagick', fps=fps)

def main():
    #env = gym.make("Taxi-v3")
    env = gym.make("Taxi-v3", render_mode="rgb_array").env

    # initialize the q-table
    state_size = env.observation_space.n
    action_size = env.action_space.n
    qtable = np.zeros((state_size, action_size))

    # set the number of episodes
    EPISODES = 1000
    STEPS_PER_EPISODE = 99
    experience_buffer = []

    # hyperparameters
    epsilon = 1.0
    decay_rate= 0.005
    learning_rate = 0.9
    discount_rate = 0.8

    for episode in range(EPISODES):
        # At the beginning of each episode, done is false
        done = False
        # reset the env for each new episode
        state, info = env.reset()
        #print(type(state))
        #print(state)
        for step in range(STEPS_PER_EPISODE):

            # in here, we have to decide whether to 
            # explore the env or exploit what we already know
            # this is where the exploration-exploitation tradeoff comes to play
            if random.uniform(0,1) < epsilon:
                # explore
                action = env.action_space.sample()
            else:
                # exploit
                action = np.argmax(qtable[state,:])

            new_state, reward, done, abort, info = env.step(action)

            # Q-learning algorithm implementation
            #print(type(state))
            #print(type(action))
            qtable[state,action] = qtable[state,action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state])-qtable[state,action])

            state = new_state

            if done or abort: 
                break

        # Decrease epsilon
        epsilon = np.exp(-decay_rate*episode)


    state, info = env.reset()
    done = False
    rewards = 0

    # this loop is for the animation so you can visually see
    # how the agent is performing.
    for s in range(STEPS_PER_EPISODE):

        print(f"TRAINED AGENT")
        print("Step {}".format(s+1))

        # exploit a known action, we'll only used the
        # exploitation since the agent is aleady trained
        action = np.argmax(qtable[state,:])
        # take the action in the environment
        new_state, reward, done, abort, info = env.step(action)
        # update reward
        rewards += reward
        # update the screenshot of the environment
        #frame = env.render()
        #plt.imshow(frame)
        #plt.axis("off")
        #plt.show()
        # Store rendered frame in animation dictionary
        experience_buffer.append({
            'frame': env.render(),
            'episode': s,
            'epoch': s,
            'state': new_state,
            'action': action,
            'reward': reward
            }
        )
        store_episode_as_gif(experience_buffer)

        print(f"score: {rewards}")
        state = new_state

        if done == True:
            break

    env.close()
    
    # Run animation and print output
    #run_animation(experience_buffer)
    


if __name__ == "__main__":
    main()

