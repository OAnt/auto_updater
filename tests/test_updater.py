import Queue
import time

import unittest

import auto_updater.updater as updater


class MiscUpdater(object):
    def set_up():
        pass

    def __init__(self):
        self.counter = 0

    def update(self, zzz):
        self.counter += 1


class TestThreadedUpdater(unittest.TestCase):
    def setUp(self):
        self.misc_updater = MiscUpdater()
        self.queue = Queue.Queue()
        self.updater = updater.ThreadedUpdater(self.queue, self.misc_updater)
        self.a_list = ['rrrr', 'aaaa', 'ttt', 'jjjj']

    def test__init__(self):
        assert(isinstance(self.updater.updater, MiscUpdater))
        assert(isinstance(self.updater.queue, Queue.Queue))

    def test_run(self):
        for item in self.a_list:
            self.queue.put(item)
        self.updater.start()
        start_time = time.time()
        while not self.queue.empty() :
            if time.time() - start_time > 1:
                self.fail("Updater did not process queue")
        self.updater.stop()
        assert(self.misc_updater.counter == len(self.a_list))
