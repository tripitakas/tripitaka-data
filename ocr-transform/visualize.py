#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from os import path, listdir
from file_util import load_json


class MainHandler(RequestHandler):
    def get(self):
        names = sorted([f[:-4] for f in listdir('cut-result') if f.endswith('.txt')])
        exists = [load_json(path.join('char-pos', *s.split('_')[:-1], s + '.json')) for s in names]
        items = ['<li><a href="/{0}">{0}</a>{1}</li>'.format(n, '' if e else ' ?') for n, e in zip(names, exists)]
        items = [s for s in items if '?' not in s] + [s for s in items if '?' in s]
        self.write('<ol>%s</ol>' % ''.join(items))


class CutHandler(RequestHandler):
    def get(self, name):
        cut = load_json(path.join('char-pos', *name.split('_')[:-1], name + '.json'))
        if not cut:
            return self.write(name + ' not exist')
        self.render('visualize.html', cut=cut)


if __name__ == '__main__':
    app = Application([(r'/', MainHandler), (r'/(\w+)', CutHandler)], debug=True)
    app.listen(8002)
    print('Start http://localhost:8002')
    IOLoop.current().start()
