"""
Matplotlib animation for the swarm.
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import List


class Visualizer:
    def __init__(self, agents: List, arena: np.ndarray, cfg: dict):
        self.agents = agents
        self.arena = arena
        self.cfg = cfg
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.scat = None

    def animate(self, dt: float, max_steps: int):
        self.ax.set_xlim(0, self.arena[0])
        self.ax.set_ylim(0, self.arena[1])
        self.ax.set_title('Distributed Swarm Simulation')
        self.scat = self.ax.scatter([], [])

        def init():
            self.scat.set_offsets([])
            return (self.scat,)

        def update(frame):
            positions = np.array([a.position for a in self.agents])
            self.scat.set_offsets(positions)
            return (self.scat,)

        ani = animation.FuncAnimation(self.fig, update, frames=range(max_steps), init_func=init, interval=dt*1000, blit=True)
        plt.show()
