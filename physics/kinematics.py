"""
2D kinematic integrator with speed clamp.
"""
import numpy as np


def integrate_step(pos: np.ndarray, vel: np.ndarray, accel: np.ndarray, dt: float, max_speed: float):
    new_vel = vel + accel * dt
    speed = np.linalg.norm(new_vel)
    if speed > max_speed:
        new_vel = new_vel * (max_speed / speed)
    new_pos = pos + new_vel * dt
    return new_pos, new_vel