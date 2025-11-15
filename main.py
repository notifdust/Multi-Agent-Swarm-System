"""
Entrypoint to run a simulation experiment locally in-process.
"""
import argparse
import yaml
from simulator.simulator import Simulator


def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', required=False, default='config/example.yaml')
    args = parser.parse_args()
    cfg = load_config(args.config)

    sim = Simulator(cfg)
    sim.run()
