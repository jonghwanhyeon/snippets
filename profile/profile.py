import sys
import time

from contextlib import contextmanager


@contextmanager
def profile(message=None):
    start_time, end_time = time.time(), 0
    yield lambda: end_time - start_time
    end_time = time.time()

    if message is not None:
        print(message.format(end_time - start_time), file=sys.stderr)


if __name__ == '__main__':
    with profile('Elapsed time: {:.2f}s'):
        for _ in range(100):
            time.sleep(1 / 100)
    # Elapsed time: 1.09s

    with profile() as elapsed:
        for _ in range(100):
            time.sleep(1 / 100)
    print(f'Elapsed time: {elapsed():.2f}s')
    # Elapsed time: 1.09s