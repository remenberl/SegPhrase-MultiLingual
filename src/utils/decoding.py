# -*- coding: utf-8 -*-

import codecs
import sys

mapping = dict()

def main(argv):
   mappingFile = argv[0]
   for line in codecs.open(mappingFile, encoding='utf-8', mode='r'):
      elements = line.split(',')
      mapping[elements[0].strip()] = elements[1].strip()
   for i in range(1, len(argv)):
         with codecs.open(argv[i] + '.natural', mode='w') as output:
            for line in codecs.open(argv[i], encoding='utf-8', mode='r'):
               newline = []
               unit = []
               for ch in line:
                  if ch.isalpha():
                     unit.append(ch)
                  else:
                     if len(unit) > 0:
                        newline.append(mapping[''.join(unit)])
                        unit = []
                     newline.append(ch)
               if len(unit) > 0:
                  newline.append(mapping[''.join(unit)])
               
               output.write(u''.join(newline).encode('utf8'))

if __name__ == "__main__":
   main(sys.argv[1 : ])