#! /home/pi/.virtualenvs/fsObs/bin/python

import pyinotify
import listener
import updater
import Queue

a_queue = Queue.Queue()
event_parser = listener.EventParser(a_queue)
parser_updater = updater.ParserUpdater('/home/pi/databases/USRDB4.db')
a_listener = listener.Listener(event_parser)
a_listener.run('/home/pi/music/Music', pyinotify.IN_CLOSE_WRITE|pyinotify.IN_DELETE)
an_updater = updater.ThreadedUpdater(a_queue, parser_updater)
an_updater.start()
#a_listener.run('/tmp', pyinotify.IN_DELETE)
