# -*- coding: utf-8 -*-

import codecs
import sys

endings = set([ch for ch in ".!?,;:()\"[]"]);

mapping = {u'０':'0', u'１':'1', u'２':'2', u'３':'3', u'４':'4', u'５':'5', u'６':'6', u'７':'7', u'８':'8', u'９':'9', \
           u'Ａ':'A', u'Ｂ':'B', u'Ｃ':'C', u'Ｄ':'D', u'Ｅ':'E', u'Ｆ':'F', u'Ｇ':'G', u'Ｈ':'H', u'Ｉ':'I', u'Ｊ':'J', \
           u'Ｋ':'K', u'Ｌ':'L', u'Ｍ':'M', u'Ｎ':'N', u'Ｏ':'O', u'Ｐ':'P', u'Ｑ':'Q', u'Ｒ':'R', u'Ｓ':'S', u'Ｔ':'T', \
           u'Ｕ':'U', u'Ｖ':'V', u'Ｗ':'W', u'Ｘ':'X', u'Ｙ':'Y', u'Ｚ':'Z', \
           u'ａ':'a', u'ｂ':'b', u'ｃ':'c', u'ｄ':'d', u'ｅ':'e', u'ｆ':'f', u'ｇ':'g', u'ｈ':'h', u'ｉ':'i', u'ｊ':'j', \
           u'ｋ':'k', u'ｌ':'l', u'ｍ':'m', u'ｎ':'n', u'ｏ':'o', u'ｐ':'p', u'ｑ':'q', u'ｒ':'r', u'ｓ':'s', u'ｔ':'t', \
           u'ｕ':'u', u'ｖ':'v', u'ｗ':'w', u'ｘ':'x', u'ｙ':'y', u'ｚ':'z', \
           u'（':'(', u'）':')', u'〔':'[', u'〕':']', u'【':'[', u'】':']', u'〖':'[', u'〗':']', u'｛':'{', u'｝':'}', \
           u'《':'<', u'》':'>', u'％':'%', u'＋':'+', u'—':'-', u'－':'-', u'～':'-', u'：':':', u'。':'.', u'、':',', \
           u'，':',', u'、':'.', u'；':';', u'？':'?', u'！':'!', u'…':'-', u'‖':'|', u'”':'"', u'‘':'\'', u'｜':'|', \
           u'〃':'"', u'　':' ', u'·':','}

def q2b(ustr):
    return ''.join([c if c not in mapping else mapping[c] for c in ustr])

def main(argv):
    rawTextInput = 'rawText.txt'
    argc = len(argv)
    for i in xrange(argc):
        if argv[i] == "-i" and i + 1 < argc:
            rawTextInput = argv[i + 1]
        elif argv[i] == "-o" and i + 1 < argc:
            segmentedFile = argv[i + 1]
    with codecs.open(segmentedFile, mode='w') as output:
        for line in codecs.open(rawTextInput, encoding='utf-8', mode='r'):
            line = q2b(line)
            output.write(line.encode('utf8'))

if __name__ == "__main__":
    main(sys.argv[1 : ])