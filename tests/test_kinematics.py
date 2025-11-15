"""
Simple unit test for kinematics.
"""
import numpy as np
from physics.kinematics import integrate_step




def test_integrate_forward():
p = np.array([0., 0.])
v = np.array([0., 0.])
a = np.array([1., 0.])
p2, v2 = integrate_step(p, v, a, 1.0, 10.0)
assert abs(p2[0] - 1.0) < 1e-6
assert abs(v2[0] - 1.0) < 1e-6