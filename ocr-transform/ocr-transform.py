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
    columns = []

    # 结束一列字
    def end_column():
        if chars and columns:
            columns[-1]['chars'] = chars[:]
        del chars[:]

    # 按X坐标对一栏中的列重新编号，按Y坐标对一列字重新编号
    def end_block():
        if columns:
            col_num = sorted([c['no'] for c in columns])
            columns.sort(key=itemgetter('x'), reverse=True)
            for i, col in enumerate(columns):
                col['no'] = col_num[i]
                cid = col['column_id'].split('c')
                cid[-1] = str(col_num[i])
                col['column_id'] = 'c'.join(cid)

                if 'chars' in col:
                    c_chars = col['chars']
                    num = sorted([c['no'] for c in c_chars])
                    c_chars.sort(key=itemgetter('y'))
                    for j, c in enumerate(c_chars):
                        c['no'] = num[j]
                        cid = c['char_id'].split('c')
                        cid[2] = str(num[j])
                        cid[1] = str(col_num[i])
                        c['char_id'] = 'c'.join(cid)
                    info['chars'].extend(c_chars)
                    del col['chars']
            info['columns'].extend(columns)
            del columns[:]

    # 读取OCR识别的每一行文字（列、字）
    for row_i, text in enumerate(lines[1:]):
        text = text.strip()
        cols = text.replace(':', ',').split(',')
        x, y, w, h = [int(s) for s in cols[:4]]
        cc = float(cols[4])

        # 找到所属栏，在栏外就丢弃
        column_now = get_block_no(blocks, x, y, w, h, txt_file, row_i)
        if not column_now:
            continue

        # 如果遇到列，则递增列号，重置字序号，栏号变了就结束前一栏
        if len(cols) > 5:
            line_no += 1
            char_no = 0
            end_column()
            if column != column_now:
                column = column_now
                line_no = 1
                end_block()

            txt = ''.join(cols[5:])
            columns.append(dict(x=x, y=y, w=w, h=h, cc=cc, txt=txt, no=line_no,
                                column_id='b%dc%d' % (column, line_no)))
        else:
            char_no += 1
            chars.append(dict(x=x, y=y, w=w, h=h, cc=cc, no=char_no,
                              char_id='b%dc%dc%d' % (column, line_no, char_no)))
    end_column()
    end_block()

    return info


def transform_files(txt_path, dst_path, only_name=None):
    """ 转换指定目录下的所有TXT文件，可以指定只转换特定前缀的文件 """
    index = {}
    for txt_file in glob(path.join(txt_path, '*.txt')):
        name = path.basename(txt_file)
        info = '_' in txt_file and (not only_name or only_name in name) and transform_file(txt_file)
        if info:
            parts = name.replace('.', '_').split('_')[:-1]
            index[parts[0]] = index.get(parts[0], []) + [(int(parts[1]), int(parts[2]), '_'.join(parts[3:]))]
            json_path = path.join(dst_path, *parts[:-1])
            create_folders(json_path)
            save_json(info, path.join(json_path, re.sub(r'\..*$', '.json', name)),
                      sort_keys=['imgname', 'imgsize', 'blocks', 'columns', 'chars'])
    for name, parts in index.items():
        parts.sort(key=itemgetter(0, 1, 2))
        index[name] = ['%s_%d_%d_%s' % (name, p[0], p[1], p[2]) for p in parts]
    save_json(index, 'index.json')


if __name__ == '__main__':
    # transform_files('cut-result', 'char-pos', 'YB_28_619')
    transform_files('cut-result', 'char-pos')
