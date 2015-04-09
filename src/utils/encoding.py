# -*- coding: utf-8 -*-

import codecs
import sys

mapping = dict()

def main(argv):
	mappingFile = argv[0]
	for line in codecs.open(mappingFile, encoding='utf-8', mode='r'):
		elements = line.split(',')
		mapping[elements[1].strip()] = elements[0].strip()
	for i in range(1, len(argv)):
   		with codecs.open(argv[i] + '.token', mode='w') as output:
   		 	for line in codecs.open(argv[i], encoding='utf-8', mode='r'):
   		 		elements = line.strip().split(' ')
   		 		all_in = True
   		 		pool = []
   		 		for element in elements:
   		 			if element not in mapping:
   		 				all_in = False
   		 				break
   		 			else:
   		 				pool.append(mapping[element])
   		 		if all_in:
   		 			for unit in pool[:-1]:
   		 				output.write(unit)
   		 				output.write(' ')
   		 			output.write(pool[-1])
   		 			output.write('\n')

if __name__ == "__main__":
    main(sys.argv[1 : ])