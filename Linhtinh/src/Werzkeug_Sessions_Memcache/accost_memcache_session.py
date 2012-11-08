# -*- coding: utf-8 -*-
__all__ = ['BDBSessionStore', 'FilesystemSessionStore', 'MemorySessionStore',
    'MemcachedSessionStore', 'GAESessionStore', 'dummy_session']
import os
try:
    from cPickle import dumps, loads, HIGHEST_PROTOCOL
except ImportError:
    from pickle import dumps, loads, HIGHEST_PROTOCOL
from werkzeug.contrib.sessions import FilesystemSessionStore, SessionStore, \
        Session


class DummySession(object):
    should_save = False
dummy_session = DummySession()


class RedisSessionStore(SessionStore):
    def __init__(self, key_prefix='', host='127.0.0.1', port=6379, dbindex=1, expire=1800):
        SessionStore.__init__(self)
        import redis
        self.redis = redis.Redis(host, port, dbindex)
        self.key_prefix = key_prefix
        self.expire = expire

    def _get_session_key(self, sid):
        return str(self.key_prefix + sid)

    def save(self, session):
        key = self._get_session_key(session.sid)
        data = dumps(dict(session), HIGHEST_PROTOCOL)
        self.redis.setex(key, data, self.expire)

    def delete(self, session):
        key = self._get_session_key(session.sid)
        self.redis.delete(key)

    def get(self, sid):
        key = self._get_session_key(sid)
        data = self.redis.get(key)
        if session is None:
            session = self.new()
        else:
            self.redis.setex(key, data, self.expire)
            session = self.session_class(loads(data), sid, False)
        return session


class FilesystemLevelSessionStore(FilesystemSessionStore):
    def __init__(self, path=None, level=1):
        self.level = level
        s = '%s/' * level
        FilesystemSessionStore.__init__(self, path,
                filename_template=s+'werkzeug_%s.sess')

    def get_session_filename(self, sid):
        args = []
        for i in range(self.level):
            args.append(sid[i])
        args.append(sid)
        return os.path.join(self.path, self.filename_template % tuple(args))


class BDBSessionStore(SessionStore):
    def __init__(self, file_path=None, session_class=Session):
        import bsddb
        SessionStore.__init__(self, session_class)
        if file_path is None:
            from tempfile import gettempdir
            file_path = os.path.join(gettempdir(), 'session.bdb')
        self.db = bsddb.hashopen(file_path)

    def save(self, session):
        self.db[str(session.sid)] = dumps(dict(session), HIGHEST_PROTOCOL)
        self.db.sync()

    def delete(self, session):
        try:
            del self.db[str(session.sid)]
        except KeyError:
            pass
        else:
            self.db.sync()

    def get(self, sid):
        session = self.db.get(str(sid))
        if not session:
            session = self.new()
        else:
            session = self.session_class(loads(session), sid, False)
        return session


class MemorySessionStore(SessionStore):
    def __init__(self, session_class=Session):
        SessionStore.__init__(self, session_class)
        self.db = {}

    def save(self, session):
        self.db[session.sid] = session

    def delete(self, session):
        self.db.pop(session.sid, None)

    def get(self, sid):
        try:
            return self.db[sid]
        except KeyError:
            return self.new()


class MemcachedSessionStore(SessionStore):
    def __init__(self, servers, session_class=Session):
        SessionStore.__init__(self, session_class)
        try:
            import cmemcache as memcache
        except ImportError:
            import memcache
        self.client = memcache.Client(servers)

    def save(self, session):
        s = dumps(dict(session), HIGHEST_PROTOCOL)
        self.client.set(str(session.sid), s)

    def delete(self, session):
        self.client.delete(str(session.sid))

    def get(self, sid):
        session = self.client.get(str(sid))
        if session is None:
            session = self.new()
        else:
            session = self.session_class(loads(session), sid, False)
        return session


class GAESessionStore(SessionStore):
    def __init__(self, session_class=Session):
        SessionStore.__init__(self, session_class)
        from google.appengine.api import memcache
        self.client = memcache
