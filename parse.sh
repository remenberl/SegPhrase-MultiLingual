TOP_K=5
OFFSET=1
export PYPY=pypy
export RAW_TEXT=data/test.txt 
export OUTPUT=results/offset.txt

opencc -i ${RAW_TEXT} -o tmp/pre_test.txt -c tw2s.json
${PYPY} src/preprocessing/punctuation.py -i tmp/pre_test.txt -o tmp/test.txt
${PYPY} src/online_query/encoding.py -i tmp/test.txt -o tmp/test.token -map results/mapping.txt -offset tmp/offset.txt
echo parsing ...
./bin/segphrase_parser results/segmentation.model results/salient.csv 20000 tmp/test.token tmp/test.parsed.txt 0 ${TOP_K} ${OFFSET}
echo decoding ...
${PYPY} src/online_query/decoding.py -i tmp/test.parsed.txt -o ${OUTPUT} -orig ${RAW_TEXT} -offset tmp/offset.txt
