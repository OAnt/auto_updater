import pyinotify
import Queue

class BasicEvent(pyinotify.ProcessEvent):
    def process_default(self, event):
        print event 


class EventParser(pyinotify.ProcessEvent):
    """
    Shared class between listener (producer) which add events and
    consumer which add to the db
    """
    def __init__(self, queue, pevent=None, **kargs):
        pyinotify.ProcessEvent.__init__(self, pevent, **kargs) 
        self.queue = queue

    def process_default(self, event):
        event_info = {'type': event.maskname,
                      'value': '{0}/{1}'.format(event.path, event.name)
                     }
        self.queue.put(event_info)


class Listener(object):
    def __init__(self, handler):
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm, default_proc_fun=handler)

    def run(self, folder, event_type):
        self.notifier.start()
        self.wm.add_watch(folder, event_type)

    def stop(self):
        self.notifier.stop()
            
