import numpy as np


class unity:
    def __init__(self):
        pass

    def __call__(self, x):
        return x

    def inverse(self, x):
        return x


class log:
    def __init__(self, base=10):
        self.base = base

    def __call__(self, x):
        return np.log(x) / np.log(self.base)

    def inverse(self, x):
        return self.base**x


class power:
    def __init__(self, slope=1):
        self.slope = slope

    def __call__(self, x):
        return x**self.slope

    def inverse(self, x):
        return x ** (1 / self.slope)
