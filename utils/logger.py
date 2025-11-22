"""
Simple CSV logger for agent positions.
"""
import os
from typing import List


class SimpleLogger:
    def __init__(self, cfg: dict):
        self.enabled = cfg.get('enabled', False)
        self.path = cfg.get('path', 'logs/run.log')
        if self.enabled:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'w') as f:
                f.write('step,' + ','.join([f'ax{i}_x,ax{i}_y' for i in range(50)]) + '\n')

    def log(self, step: int, positions: List):
        if not self.enabled:
            return
        # positions: list of np arrays
        with open(self.path, 'a') as f:
            row = [str(step)]
            for p in positions:
                row.append(str(float(p[0])))
                row.append(str(float(p[1])))
            f.write(','.join(row) + '\n')