# -*- coding: utf-8 -*-

import codecs
import jieba
import sys

punctuations = u'()[]{}<>%+-:.,;!|"\''

mapping = dict()
index = 'abcdefghijklmnopqrstuvwxyz'
def id2alpha(id):
  alpha = ''
  if id == 0:
    return 'a'
  while id > 0:
    alpha = index[id % 26] + alpha
    id = id / 26
  return alpha

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
    with codecs.open(tokenizedFile, encoding='utf-8', mode='w') as output:
        id = 0
        for line in codecs.open(rawTextInput, encoding='utf-8', mode='r'):
            result = jieba.tokenize(line.strip())
            newline = []
            for tk in result:
                tk = tk[0]
                if tk == ' ':
                    newline.append(' ')
                    continue
                if tk in punctuations:
                    newline.append(tk)
                    continue
                tk = ''.join([i for i in tk if not i.isdigit()]).lower()
                if len(tk) == 0:
                    newline.append(' ')
                    continue
                if tk not in mapping:
                    mapping[tk] = id2alpha(id)
                    id += 1
                newline.append(mapping[tk])
                newline.append(' ')
            output.write(u''.join(newline).encode('utf8'))
            output.write('\n')
    with codecs.open(mappingFile, encoding='utf-8', mode='w') as output:
        for (string, token) in mapping.iteritems():
            output.write(token.encode('utf8'))
            output.write(',')
            output.write(string)
            output.write('\n')

if __name__ == "__main__":
    main(sys.argv[1 : ])