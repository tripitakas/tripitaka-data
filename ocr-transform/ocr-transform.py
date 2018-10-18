#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于 block-pos/**/*.json 栏切分数据，将OCR文本 cut-result/*.txt 转换为 char-pos 下的列切分和字切分的JSON文件.

import re
from os import path
from glob import glob
from file_util import create_folders, load_json, save_json
from operator import itemgetter


def get_block_json(filename):
    """ 得到页面文件名对应的栏切分数据 """
    filename = path.basename(filename)
    filename = path.join('block-pos', *filename.split('_')[:-1], re.sub(r'\..*$', '.json', filename))
    return load_json(filename, True)


def get_block_no(blocks, x, y, w, h, filename, row_i):
    """ 根据框坐标查找所属的栏的序号，0为找不到 """
    for i, b in enumerate(blocks):
        if x > b['x'] - w / 3 and x + w < b['x'] + b['w'] + w / 3 and \
                y > b['y'] - h / 3 and y + h < b['y'] + b['h'] + h / 3:
            return i + 1
    print('block not found: %s, %s' % (filename, str([x, y, w, h, row_i + 2])))
    return 0


def transform_file(txt_file):
    """ 处理OCR文本，输出列切分和字切分的JSON文件 """
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
    chars = []

    # 按Y坐标对一列字重新编号
    def end_column():
        if chars:
            num = sorted([c['no'] for c in chars])
            for i, c in enumerate(sorted(chars, key=itemgetter('y'))):
                c['no'] = num[i]
                cid = c['char_id'].split('c')
                cid[-1] = str(num[i])
                c['char_id'] = 'c'.join(cid)
            info['chars'].extend(chars)
            del chars[:]

    # 读取OCR识别的每一行文字（列、字）
    for row_i, text in enumerate(lines[1:]):
        text = text.strip()
        cols = text.replace(':', ',').split(',')
        x, y, w, h = [int(s) for s in cols[:4]]
        cc = float(cols[4])

        # 遇到列，则递增列号，准备重置字序号
        if len(cols) > 5:
            line_no += 1
            column = 0

        # 找到所属栏，栏号变了就重置字序号
        column_now = get_block_no(blocks, x, y, w, h, txt_file, row_i)
        if column != column_now or not column:
            column = column_now
            char_no = 0
            end_column()

        if len(cols) > 5:
            end_column()
            txt = ''.join(cols[5:])
            info['columns'].append(dict(x=x, y=y, w=w, h=h, cc=cc, txt=txt, no=line_no,
                                        column_id='b%dc%d' % (column, line_no)))
        else:
            char_no += 1
            chars.append(dict(x=x, y=y, w=w, h=h, cc=cc, no=char_no,
                              char_id='b%dc%dc%d' % (column, line_no, char_no)))
    end_column()

    return info


def transform_files(txt_path, dst_path, only_name=None):
    """ 转换指定目录下的所有TXT文件，可以指定只转换特定前缀的文件 """
    for txt_file in glob(path.join(txt_path, '*.txt')):
        name = path.basename(txt_file)
        info = '_' in txt_file and (not only_name or only_name in name) and transform_file(txt_file)
        if info:
            json_path = path.join(dst_path, *name.split('_')[:-1])
            create_folders(json_path)
            save_json(info, path.join(json_path, re.sub(r'\..*$', '.json', name)))


if __name__ == '__main__':
    # transform_files('cut-result', 'char-pos', 'GL_1047_1_21')
    transform_files('cut-result', 'char-pos')
