#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from os import path, listdir
from file_util import load_json


class MainHandler(RequestHandler):
    def get(self):
        names = sorted([f[:-4] for f in listdir('cut-result') if f.endswith('.txt')])
        self.write('<ol>%s</ol>' % ''.join(['<li><a href="/{0}">{0}</a></li>'.format(n) for n in names]))


class CutHandler(RequestHandler):
    def get(self, name):
        cut = load_json(path.join('char-pos', *name.split('_')[:-1], name + '.json'))
        blocks = load_json(path.join('block-pos', *name.split('_')[:-1], name + '.json'))
        if not cut or not blocks:
            return self.write(name + ' not exist')
        blocks = blocks['blocks']
        self.render('visualize.html', cut=cut, blocks=blocks)


if __name__ == '__main__':
    app = Application([(r'/', MainHandler), (r'/(\w+)', CutHandler)], debug=True)
    app.listen(8002)
    print('Start http://localhost:8002')
    IOLoop.current().start()
