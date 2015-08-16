# -*- coding: utf-8 -*-

import codecs
import jieba
import sys

punctuations = u'=^&#\\_*?/()[]{}<>%+-:.,;!|"\''

mapping = dict()

def main(argv):
    rawTextInput = 'rawText.txt'
    argc = len(argv)
    for i in xrange(argc):
        if argv[i] == "-i" and i + 1 < argc:
          rawTextInput = argv[i + 1]
        elif argv[i] == "-o" and i + 1 < argc:
          tokenizedFile = argv[i + 1]
        elif argv[i] == "-map" and i + 1 < argc:
          mappingFile = argv[i + 1]
        elif argv[i] == "-offset" and i + 1 < argc:
          offsetFile = argv[i + 1]
    with codecs.open(mappingFile, encoding='utf-8', mode='r') as input:
        for line in input:
            elements = line.rstrip().split(',')
            mapping[elements[1]] = elements[0]

    outputA = codecs.open(tokenizedFile, encoding='utf-8', mode='w')
    outputB = codecs.open(offsetFile, encoding='utf-8', mode='w')
    shift = 0
    shift_in_orig_file = 0
    for line in codecs.open(rawTextInput, encoding='utf-8', mode='r'):
        offsets = []
        result = jieba.tokenize(line.rstrip())
        newline = []
        for tk in result:
            begin = tk[1] + shift_in_orig_file
            end = tk[2] + shift_in_orig_file
            tk = tk[0]
            if tk == ' ':
                newline.append(' ')
                shift += 1
                continue
            if tk in punctuations:
                newline.append(tk)
                shift += len(tk)
                continue
            tk = ''.join([i for i in tk if not i.isdigit()]).lower()
            if len(tk) == 0:
                newline.append(' ')
                shift += 1
                continue
            if tk not in mapping:
                shift += len('zzzzzzzzzzz')
                newline.append('zzzzzzzzzzz')
            else:
                newline.append(mapping[tk])
                # the second and third elements indicate the offset in the encoded text
                # the fourth and fifth elements indicate the offset in the orignal text
                offsets.append((tk, shift, shift + len(mapping[tk]), begin, end))
                shift += len(mapping[tk])
            newline.append(' ')
            shift += 1
        outputA.write(u''.join(newline).encode('utf8'))
        outputA.write('\n')
        for (string, begin1, end1, begin2, end2) in offsets:
            outputB.write(string)
            outputB.write(',')
            outputB.write(str(begin1))
            outputB.write(',')
            outputB.write(str(end1))
            outputB.write(',')
            outputB.write(str(begin2))
            outputB.write(',')
            outputB.write(str(end2))
            outputB.write('\t')
        outputB.write('\n')
        shift_in_orig_file += len(line)

if __name__ == "__main__":
    main(sys.argv[1 : ])
