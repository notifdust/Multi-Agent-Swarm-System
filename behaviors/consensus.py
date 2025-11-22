"""
Simple average consensus on a scalar estimate carried by each agent. Example usage: consensus on heading or target estimate.
"""
from typing import Dict


def consensus_update(local_value: float, neighbor_values: Dict[int, float], alpha: float = 0.5) -> float:
    # neighbors provided as {id: value}
    if not neighbor_values:
        return local_value
    avg = sum(neighbor_values.values()) / len(neighbor_values)
    return (1 - alpha) * local_value + alpha * avg