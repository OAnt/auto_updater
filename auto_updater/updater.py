import threading
import Queue
import sqlite3
import os.path

import kaa.metadata
import kaa.metadata.core


EXIT = object()


class BaseUpdater(object):
    def set_up(self):
        pass

    def update(self, new_file):
        print new_file


class DatabaseObject(object):
    def __init__(self, db_path):
        self.path = db_path

    def connect(self):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

    def _execute(self, statement, values):
        self.cursor.execute(statement, values)
        result = self.cursor.fetchall()
        return result

    def insert(self, metadata, path):
        statement = 'SELECT id FROM artists WHERE name=?'
        artist_id = self._execute(statement, [metadata.get('artist', default='unknown')])
        if not artist_id:
            statement = 'INSERT INTO artists (name) VALUES (?)'
            self._execute(statement, [metadata.get('artist', default='unknown')])
            artist_id = self.cursor.lastrowid
            self.db.commit()
        else:
            artist_id = artist_id[0][0]
        statement = 'SELECT id FROM albums WHERE album=?'
        album_id = self._execute(statement, [metadata.get('album', default='unknown')])
        if album_id:
            album_id = album_id[0][0]
        else:
            statement = 'INSERT INTO albums (album, artist_id) VALUES (?, ?)'
            self._execute(statement, [metadata.get('album', default='unknown'), artist_id])
            album_id = self.cursor.lastrowid
            self.db.commit()
        a_path = os.path.basename(path)
        print a_path
        statement = 'INSERT INTO Songs (song, album_id, path, Album, Artist) VALUES (?, ?, ?, ?, ?)'
        self._execute(statement, [metadata.get('title', default='unknown'), album_id, a_path, metadata.get('album', default='unknown'), metadata.get('artist', default='unknown')])
        self.db.commit()

    def delete_path(self, path):
        pass


class ParserUpdater(object):
    def __init__(self, db_path):
        self.db_path = db_path

    def set_up(self):
        self.db = DatabaseObject(self.db_path)
        self.db.connect()

    def update(self, task):
        if task['type'] == 'IN_CREATE':
            self.add_song(task['value'])
        elif task['type'] == 'IN_DELETE':
            self.rm_song(task['value'])

    def add_song(self, song_file):
        try:
            info = kaa.metadata.parse(song_file)
        except kaa.metadata.core.ParseError as e:
            return
        self.db.insert(info, song_file)

    def rm_song(self, song_file):
        self.db.delete_path(song_file)


class ThreadedUpdater(threading.Thread):
    def __init__(self, queue, updater):
        threading.Thread.__init__(self)
        self.queue = queue
        self.updater = updater
    
    def run(self):
        self.updater.set_up()
        while 1:
            task = self.queue.get(True, None)
            if task is EXIT:
                break
            self.updater.update(task)

    def stop(self):
        self.queue.put(EXIT)
