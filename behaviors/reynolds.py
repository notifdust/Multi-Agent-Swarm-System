"""
Classic Reynolds rules (separation, alignment, cohesion).
"""
from typing import Dict, Any
import numpy as np


def reynolds_force(agent, neighbor_states: Dict[int, Dict[str, Any]], params: Dict[str, float]):
    pos = agent.position
    vel = agent.velocity
    neigh_radius = params.get('neighbor_radius', 2.5)
    sep_w = params.get('separation_weight', 1.2)
    ali_w = params.get('alignment_weight', 1.0)
    coh_w = params.get('cohesion_weight', 0.8)

    neighbors = []
    for sid, st in neighbor_states.items():
        rel = np.array(st['position']) - pos
        dist = np.linalg.norm(rel)
        if dist <= neigh_radius and dist > 1e-6:
            neighbors.append((sid, rel, dist, np.array(st['velocity'])))

    if not neighbors:
        return np.zeros(2)

    # separation
    sep = np.zeros(2)
    for _sid, rel, dist, _v in neighbors:
        sep -= (rel / (dist**2 + 1e-6))

    # alignment
    avg_vel = np.mean([v for _sid, _rel, _dist, v in neighbors], axis=0)
    ali = avg_vel - vel

    # cohesion
    avg_pos = np.mean([pos + rel for _sid, rel, _dist, _v in neighbors], axis=0)
    coh = avg_pos - pos

    force = sep_w * sep + ali_w * ali + coh_w * coh
    return force