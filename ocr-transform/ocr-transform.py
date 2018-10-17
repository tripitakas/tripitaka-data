#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from os import path, mkdir
from glob import glob


def create_folders(filename, level=3):
    if level > 0:
        create_folders(path.dirname(filename), level - 1)
    if filename and not path.exists(filename):
        mkdir(filename)


def load_json(filename, warning=False):
    if path.exists(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except Exception as e:
            print(filename, e)
    elif warning:
        print('%s not exist' % filename)


def save_json(obj, filename, sort_keys=False):
    with open(filename, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=sort_keys)


def get_block_json(filename):
    filename = path.basename(filename)
    filename = path.join('block-pos', *filename.split('_')[:-1], re.sub(r'\..*$', '.json', filename))
    return load_json(filename, True)


def get_block_no(blocks, x, y, w, h, filename):
    for i, b in enumerate(blocks):
        if x > b['x'] - 5 and y > b['y'] - 5 and x + w < b['x'] + b['w'] + 5 and y + h < b['y'] + b['h'] + 5:
            return i + 1
    print('block not found: %s, %s' % (filename, str([x, y, w, h])))
    return 0


def transform_file(txt_file):
    with open(txt_file) as f:
        lines = f.readlines()

    pos = get_block_json(txt_file)
    if not pos:
        print('%s no block-pos' % txt_file)
        return
    blocks = pos['blocks']

    info = dict(columns=[], chars=[], imgname=pos['imgname'], imgsize=pos['imgsize'])
    info['blocks'] = [dict(b, **dict(no=i + 1, cc=1, block_id='b%d' % (i + 1))) for i, b in enumerate(blocks)]
    column = 0
    line_no = 0
    char_no = 0

    for text in lines[1:]:
        text = text.strip()
        cols = text.replace(':', ',').split(',')
        x, y, w, h = [int(s) for s in cols[:4]]
        cc = float(cols[4])

        column_now = get_block_no(blocks, x, y, w, h, txt_file)
        if column != column_now:
            column = column_now
            line_no = 0

        if len(cols) > 5:
            txt = ''.join(cols[5:])
            line_no += 1
            char_no = 0
            info['columns'].append(dict(x=x, y=y, w=w, h=h, cc=cc, txt=txt, no=line_no,
                                        column_id='b%dc%d' % (column, line_no)))
        else:
            char_no += 1
            info['chars'].append(dict(x=x, y=y, w=w, h=h, cc=cc, no=char_no,
                                      char_id='b%dc%dc%d' % (column, line_no, char_no)))
    return info


def transform_files(txt_path):
    for txt_file in glob(path.join(txt_path, '*.txt')):
        info = '_' in txt_file and transform_file(txt_file)
        if info:
            name = path.basename(txt_file)
            json_path = path.join('pos', *name.split('_')[:-1])
            create_folders(json_path)
            save_json(info, path.join(json_path, re.sub(r'\..*$', '.json', name)))


if __name__ == '__main__':
    transform_files('.')
