import multiprocessing
import functools
manager = multiprocessing.Manager()

import time

from multiprocessing import JoinableQueue
from multiprocessing.context import Process


class Renderer:
#https://docs.python.org/3/library/queue.html
    def __init__(self, nb_workers=4):
        self.queue = JoinableQueue()
        self.queue2 = JoinableQueue()
        self.manager = multiprocessing.Manager()
        self.shared_list = self.manager.list()
        for a in range(0,20):
            self.shared_list.append(a)
        self.processes = [Process(target=self.upload, args=[self.shared_list]) for i in range(nb_workers)]
        for p in self.processes:
            p.start()

    def render(self, item):
        self.queue.put(item)

    def upload(self, l):
        while True:
            item = self.queue.get()
            if item is None:
                break
            try:
                print("v",l)
                id = l.index(item)
                del l[id]
                print("n",l)
                self.queue2.put(id)
            except ValueError:
                print("Not found")
                print(l)
                pass

            self.queue.task_done()
    
    def download(self):
        while True:
            item = self.queue2.get()
            if item is None:
                break
            print(item)
            self.queue2.task_done()

    def terminate(self):
        """ wait until queue is empty and terminate processes """
        self.queue.join()
        for p in self.processes:
            p.terminate()

r = Renderer()
r.render(5)
r.render(5)
r.download()
r.download()
r.terminate()





















# Q = manager.Queue()

# def stack(b, c):
#     time.sleep(3)
#     b.put(56)

# a = [56, 45, 76]
# shared_list = manager.list(a)

# pool = multiprocessing.Pool(4)
# result = pool.map(functools.partial(stack, Q), a)
# pool.close()
# pool.join()

# print(Q.get())