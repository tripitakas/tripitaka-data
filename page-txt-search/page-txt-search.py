#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fuzzywuzzy import fuzz, process


def search_text(sutra_txt, ocr_txt):
    cmp_txt = []
    ocr_i = s_i = 0
    while ocr_i < len(ocr_txt):
    for i in range():
        text = ocr_txt[i: i+4]
        r = fuzz.partial_ratio(text, sutra_txt)
        if r > 70:
            print('%s\t%d' % (text, r))


if __name__ == '__main__':
    T0278 = open('T0278.txt').read()
    search_text(T0278, open('LC_79_1_1.txt').read())
    # assert search_text(T0278, open('LC_79_1_1.txt').read()) == open('cmp-txt/LC_79_1_1.txt').read()
