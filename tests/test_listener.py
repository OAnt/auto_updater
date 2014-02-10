import os
import unittest
import time
import Queue

import pyinotify

import auto_updater.listener as listener


class DummyEvent(pyinotify.ProcessEvent, Queue.Queue):
    def __init__(self):
        pyinotify.ProcessEvent.__init__(self)
        Queue.Queue.__init__(self)

    def process_default(self, event):
        self.put(True)


class DummyChainEvent(pyinotify.ProcessEvent):
    def my_init(self, a_queue):
        self.queue = a_queue

    def process_default(self, event):
        self.queue.put(True)


class TestListener(unittest.TestCase):
    def setUp(self):
        self.a_dir = '/tmp/test_auto_updater'
        self.a_file = self.a_dir + '/tempfile'
        os.mkdir(self.a_dir)
        self.event = DummyEvent()
        self.listener = listener.Listener(self.event) 
        self.listener.run(self.a_dir, pyinotify.IN_CREATE)

    def test___init__(self):
        assert(isinstance(self.listener.notifier.proc_fun(), DummyEvent))

    def test_run(self):
        f = open(self.a_file, 'w')
        f.close()
        os.remove(self.a_file)
        res = self.event.get()
        assert(res)

    def tearDown(self):
        self.listener.stop()
        os.rmdir(self.a_dir)


class TestEventParser(unittest.TestCase):
    def setUp(self):
        self.a_dict = {'mask': pyinotify.IN_CREATE,  
                  'path': '/tmp/',
                  'name': 'filename'}
        self.event = pyinotify.Event(self.a_dict)

    def test_process_default(self):
        event_parser = listener.EventParser(Queue.Queue())
        event_parser.process_default(self.event)
        parsed_event = event_parser.queue.get()
        assert(parsed_event['type'] == 'IN_CREATE')
        assert(parsed_event['value'] == self.event.path + '/' +  self.event.name)

#    def test_chaining(self): // I think i need a listner for chaining
#        _queue = Queue.Queue()
#        event_parser = listener.EventParser(DummyChainEvent(a_queue=_queue))        
#        event_parser.process_default(self.event)
#        res = _queue.get()
#        assert(res)

