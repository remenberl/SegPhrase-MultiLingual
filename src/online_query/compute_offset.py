# -*- coding: utf-8 -*-

import codecs
import re
import sys

def main(argv):
    if (len(argv) != 2):
        print "[Usage] <input-parsed-file> <output-offset-file>"
        return
    input_file = argv[0]
    output_file = argv[1]

    content = ""
    results = 'Offsets:\n'
    with codecs.open(input_file, encoding='utf8', mode='r') as input:
        offset = 0
        bias = 0
        for line in input:
            content += re.sub('[\[\]]', '', line)
            for char in line:
                if char == '[':
                    left = offset + 1
                if char == ']':
                    right = offset
                    bias += 1
                    results += '[' + str(left - bias * 2 + 1) + ', ' + str(right - bias * 2 + 1) + ']'
                    results += ' (' + content[left - bias * 2 + 1:right - bias * 2 + 1] + ');\n'
                offset += 1
    with codecs.open(output_file, encoding='utf8', mode='w') as output:
        output.write(content)
        output.write('\n')
        output.write(results)

if __name__ == "__main__":
    main(sys.argv[1 : ])
