# -*- coding: utf-8 -*-

from itertools import izip
import codecs
import sys

punctuations = u'=^&#\\_*?/()[]{}<>%+-:.,;!|"\''

mapping = dict()

def main(argv):
    argc = len(argv)
    for i in xrange(argc):
        if argv[i] == "-i" and i + 1 < argc:
          segmentedFile = argv[i + 1]
        elif argv[i] == "-o" and i + 1 < argc:
          decodedFile = argv[i + 1]
        elif argv[i] == "-orig" and i + 1 < argc:
          origFile = argv[i + 1]
        elif argv[i] == "-map" and i + 1 < argc:
          mappingFile = argv[i + 1]
        elif argv[i] == "-offset" and i + 1 < argc:
          offsetFile = argv[i + 1]

    with codecs.open(mappingFile, encoding='utf-8', mode='r') as input:
        for line in input:
            elements = line.strip().split(',')
            mapping[elements[0]] = elements[1]

    fileA = codecs.open(origFile, encoding='utf-8', mode='r')
    fileB = codecs.open(segmentedFile, encoding='utf-8', mode='r')
    fileC = codecs.open(offsetFile, encoding='utf-8', mode='r')
    with codecs.open(decodedFile, encoding='utf-8', mode='w') as output:
        for lineA, lineB, lineC in izip(fileA, fileB, fileC):
            offset = []
            elements = lineC.strip().split('\t')
            for element in elements:
                offset.append(element.split(','))
            unit = []
            is_salient = False
            index = 0
            brackets = []
            for ch in lineB:
                if ch.isalpha():
                    unit.append(ch)
                else:
                    if ch == ']':
                        is_salient = False
                        phrase = ''.join(unit)
                        num_mapped_units = 0
                        for element in phrase.split(' '):
                            if element.strip() != '':
                                num_mapped_units += 1
                        # mapped_units = []
                        # for element in phrase.split(' '):
                        #     mapped_units.append(mapping[''.join(element)])
                        brackets.append((offset[index][1], offset[index + num_mapped_units - 1][2]))
                        index += num_mapped_units
                        unit = []
                    if is_salient:
                        if ch not in punctuations:
                            unit.append(ch)
                    elif len(unit) > 0:
                        unit = []
                        index += 1
                    if ch == '[':
                        is_salient = True
            index = 0
            output_line = ''
            for bracket in brackets:
                output_line += lineA[index:int(bracket[0])]
                output_line += '[' + lineA[int(bracket[0]):int(bracket[1])] + ']'
                index = int(bracket[1])
            output_line += lineA[index:]
            output.write(output_line)

if __name__ == "__main__":
    main(sys.argv[1 : ])
