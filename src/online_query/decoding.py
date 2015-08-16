# -*- coding: utf-8 -*-

from itertools import izip
import codecs
import sys

punctuations = u'=^&#\\_*?/()[]{}<>%+-:.,;!|"\''

token_index = []

def main(argv):
    argc = len(argv)
    for i in xrange(argc):
        if argv[i] == "-i" and i + 1 < argc:
          segmentedFile = argv[i + 1]
        elif argv[i] == "-o" and i + 1 < argc:
          decodedFile = argv[i + 1]
        elif argv[i] == "-orig" and i + 1 < argc:
          origFile = argv[i + 1]
        elif argv[i] == "-offset" and i + 1 < argc:
          offsetFile = argv[i + 1]

    fileA = codecs.open(origFile, encoding='utf-8', mode='r')
    fileB = codecs.open(segmentedFile, encoding='utf-8', mode='r')
    fileC = codecs.open(offsetFile, encoding='utf-8', mode='r')
    with open(decodedFile, 'w') as output:
        with open(origFile, 'r') as input:
            for line in input:
                output.write(line)
        with open(offsetFile, 'r') as input:
            for line in input:
                elements = line.split('\t')
                for element in elements:
                    element = element.strip()
                    if element == "":
                        continue
                    tokens = element.split(',')
                    for i in range(1, 5):
                        tokens[i] = int(tokens[i])
                    token_index.append(tokens)
        tokens_begin = 0
        with open(segmentedFile, 'r') as input:
            start = False
            for line in input:
                if start:
                    index1 = line.find(',')
                    begin = int(line[1:index1])
                    index2 = line.find(')')
                    end = int(line[index1+1:index2])
                    content = ""
                    offset = []
                    tokens_begin_cp = tokens_begin
                    while tokens_begin_cp < len(token_index):
                        if token_index[tokens_begin_cp][1] >= begin and \
                                token_index[tokens_begin_cp][2] <= end:
                            content += token_index[tokens_begin_cp][0]
                            offset.append(token_index[tokens_begin_cp][3])
                            offset.append(token_index[tokens_begin_cp][4])
                        if token_index[tokens_begin_cp][2] <= end:
                            tokens_begin_cp += 1
                            continue
                        else:
                            break
                    # moves original tokens_begin
                    while tokens_begin < len(token_index):
                        if token_index[tokens_begin][1] < begin:
                            tokens_begin += 1
                        else:
                            break
                    output.write("[")
                    output.write(str(offset[0]))
                    output.write(", ")
                    output.write(str(offset[len(offset)-1]))
                    output.write("] (")
                    output.write(content)
                    output.write(");\n")
                    continue
                if line.strip() != "Offset:":
                    continue
                else:
                    output.write('\n')
                    output.write(line)
                    start = True


if __name__ == "__main__":
    main(sys.argv[1 : ])
