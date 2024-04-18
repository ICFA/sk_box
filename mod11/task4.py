from queue import PriorityQueue
from threading import Thread
from time import sleep
from random import uniform

class Producer(Thread):
    
    def __init__(self):
        super().__init__()
        print('Producer: Running')

    def run(self):
        global queue
        for i in range(0, 6):
            queue.put(i)
            time = uniform(0.01, 1)
            sleep(time)

class Consumer(Thread):
    
    def __init__(self):
        super().__init__()
        print('Consumer: Running')

    def run(self):
        global queue
        while queue:
            i = queue.get()
            time = uniform(0.01, 1)
            sleep(time)
            print(f'running Task(priority={i}).      sleep({time})')
            queue.task_done()

queue = PriorityQueue()
producer = Producer()
consumer = Consumer()

Thread(target=producer.run).start()
Thread(target=consumer.run, daemon=True).start()
queue.join()
print('Producer: Done')
print('Consumer: Done')
