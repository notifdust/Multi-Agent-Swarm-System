"""
High-level in-process simulator that instantiates agents and runs them concurrently using asyncio.
"""
from __future__ import annotations
import asyncio
import os
import time
import math
import numpy as np
from typing import Dict, Any, List
from agents.agent import Agent
from utils.logger import SimpleLogger
from visualization.visualize import Visualizer


class Simulator:
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.num_agents = cfg.get('num_agents', 8)
        self.arena = np.array(cfg.get('arena_size', [10.0, 10.0]))
        self.sim_dt = cfg.get('sim_dt', 0.05)
        self.max_steps = cfg.get('max_steps', 1000)
        self.agents: List[Agent] = []
        self.logger = SimpleLogger(cfg.get('logging', {}))

        # spawn agents in a grid
        rng = np.random.RandomState(42)
        for i in range(self.num_agents):
            pos = rng.rand(2) * (self.arena - 2.0) + 1.0
            a = Agent(i, pos, cfg)
            # small random initial velocity
            a.velocity = (rng.rand(2) - 0.5) * 0.2
            self.agents.append(a)

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
    # start all agents
        tasks = [asyncio.create_task(a.start()) for a in self.agents]
        vis = Visualizer(self.agents, self.arena, self.cfg)
    
        # Start visualizer in executor so it doesn't block
        loop = asyncio.get_event_loop()
        #  FIX: Keep a reference to the visualization task
        vis_task = loop.run_in_executor(None, vis.animate, self.sim_dt, self.max_steps) 

        # main loop for logging
        #  FIX: The 'start' line is removed as it was unused.
        step = 0
        try:
            while step < self.max_steps:
                # log positions
                positions = [a.position.copy() for a in self.agents]
                self.logger.log(step, positions)
            await asyncio.sleep(self.sim_dt)
            step += 1
        except KeyboardInterrupt:
            pass
        finally:
        # stop agents
            for a in self.agents:
                a.stop()
        
        # cancel agent tasks
            for t in tasks:
                t.cancel()
            
        # 💡 FIX: Cancel the visualization task as well.
            vis_task.cancel() 
        
        # wait briefly
            await asyncio.sleep(0.1)
