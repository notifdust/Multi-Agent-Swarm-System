"""
Agent runtime: state, simple async loop to process incoming messages and compute control.
"""
from __future__ import annotations
import asyncio
import math
import time
from typing import List, Tuple, Dict, Any
import numpy as np
from comms.udp_comms import UDPComms
from behaviors.reynolds import reynolds_force
from physics.kinematics import integrate_step


class Agent:
    def __init__(self, aid: int, init_pos: np.ndarray, cfg: Dict[str, Any]):
        self.id = aid
        self.position = init_pos.astype(float)
        self.velocity = np.zeros(2, dtype=float)
        self.accel = np.zeros(2, dtype=float)
        self.cfg = cfg
        self.neighbor_states: Dict[int, Dict[str, Any]] = {}
        # comms binds to port base + id
        port = cfg.get('comm_port_base', 10000) + aid
        self.comms = UDPComms('127.0.0.1', port)
        self.running = False

    async def start(self):
        self.running = True
        # launch listener
        asyncio.create_task(self._listener())
        while self.running:
            t0 = time.time()
            # compute control using behaviors
            force = reynolds_force(self, self.neighbor_states, self.cfg['behavior']['params'])
            # simple acceleration limiting
            max_accel = self.cfg['controller'].get('max_accel', 1.0)
            norm = np.linalg.norm(force)
            if norm > max_accel:
                force = force * (max_accel / norm)
            self.accel = force
            # integrate
            dt = self.cfg.get('sim_dt', 0.05)
            self.position, self.velocity = integrate_step(self.position, self.velocity, self.accel, dt, self.cfg['controller']['max_speed'])
            # broadcast state
            msg = self._state_message()
            await self.comms.broadcast(msg)
            # small sleep to yield
            wait = max(0.0, dt - (time.time() - t0))
            await asyncio.sleep(wait)

    async def _listener(self):
        async for pkt in self.comms.receive_loop():
            try:
                src, data = pkt
                # parse data (expected dict)
                sid = data.get('id')
                if sid == self.id:
                    continue
                self.neighbor_states[sid] = {
                    'position': np.array(data['position']),
                    'velocity': np.array(data['velocity']),
                    'timestamp': data['t']
                }
            except Exception:
                continue

    def _state_message(self):
        return {'id': self.id, 'position': self.position.tolist(), 'velocity': self.velocity.tolist(), 't': time.time()}

    def stop(self):
        self.running = False
        self.comms.close()
