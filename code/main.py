from solver import Solver
import random
from config import Config
import time


if __name__ == '__main__':
    start = time.time()
    s = Solver()
    # s.solve()
    s.heuristic_solve()
    print("Solution Time：", time.time() - start, "seconds")

