import logging
import threading
import random
import time
from threading import Lock

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class Philosopher(threading.Thread):

    def __init__(self, left_fork: threading.Lock, right_fork: threading.Lock):
        super().__init__()
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            logger.info(f'Philosopher {self.getName()} is thinking')
            time.sleep(random.randint(1, 10))
            logger.info(f'Philosopher {self.getName()} is hungry')
            try:
                with self.left_fork, self.right_fork:
                    logger.info(f'Philosopher {self.getName()} acquired forks and is dining')
                    self.dining()
            except threading.ThreadError:
                continue

    def dining(self):
        logger.info(f'Philosopher {self.getName()} starts eating')
        time.sleep(random.randint(1, 10))
        logger.info(f'Philosopher {self.getName()} finishes eating and leaves to think')

def main():
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [Philosopher(forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(200)
    Philosopher.running = False
    logger.info(f'Now we are finishing')

if __name__ == "__main__":
    main()