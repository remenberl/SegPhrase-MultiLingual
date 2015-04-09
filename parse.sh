export PYPY=pypy
export RAW_TEXT=data/test.txt

opencc -i ${RAW_TEXT} -o tmp/pre_test.txt -c tw2s.json
${PYPY} src/preprocessing/punctuation.py -i tmp/pre_test.txt -o tmp/test.txt
${PYPY} src/online_query/encoding.py -i tmp/test.txt -o tmp/test.token -map results/mapping.txt -offset tmp/offset.txt
./bin/segphrase_parser results/segmentation.model results/salient.csv 50000 tmp/test.token tmp/test.parsed.txt 0
${PYPY} src/online_query/decoding.py -i tmp/test.parsed.txt -o tmp/test.result -map results/mapping.txt -orig ${RAW_TEXT} -offset tmp/offset.txt

${PYPY} src/online_query/compute_offset.py tmp/test.result results/offset.txt
