#!/usr/bin/env python3

import time
from grid_filter import sum_of_squares_rs

if __name__ == "__main__":
    n = 1_000_001
    t0 = time.time()
    ss1 = sum_of_squares_rs(list(range(n)))
    t1 = time.time()
    print(f'sum of squares: {ss1}, time: {t1 - t0}')
    t2 = time.time()
    ss2 = sum(i*i for i in range(n))
    t3 = time.time()
    print(f'sum of squares: {ss2}, time: {t3 - t2}')
