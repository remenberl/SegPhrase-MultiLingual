# -*- coding: utf-8 -*-

import codecs
import sys

mapping = dict()


def main(argv):
    mappingFile = argv[0]
    for line in codecs.open(mappingFile, encoding='utf-8', mode='r'):
        elements = line.split(',')
        mapping[elements[0].strip()] = elements[1].strip()

    phraseListFile = argv[1]
    outputFile = argv[2]
    cleaned_results = []
    with codecs.open(outputFile, mode='w') as output:
        for line in codecs.open(phraseListFile, encoding='utf-8', mode='r'):
            elements = line.split(',')
            units = list()
            for unit in elements[0].split('_'):
                if unit.strip() != '' and unit in mapping:
                    units.append(mapping[unit])
            phrase = '_'.join(units)
            score = elements[1]
            if len(phrase) <= 1:
                continue
            output.write(u','.join([phrase, score]).encode('utf8'))
            cleaned_results.append(line)
    with codecs.open(phraseListFile, mode='w') as output:
        for line in cleaned_results:
            output.write(line)

if __name__ == "__main__":
    main(sys.argv[1:])
