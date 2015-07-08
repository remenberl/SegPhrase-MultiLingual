export PYPY=pypy
export RAW_TEXT=data/test2.txt

cd stanford-segmenter
java -mx1g -classpath stanford-segmenter-3.5.2.jar \
     edu.stanford.nlp.international.arabic.process.ArabicSegmenter \
     -loadClassifier data/arabic-segmenter-atb+bn+arztrain.ser.gz \
     -orthoOptions normArDigits,normArPunc  \
     -textFile ../$RAW_TEXT > ../tmp/test.txt
cd ..

${PYPY} src/online_query/encoding.py -i tmp/test.txt -o tmp/test.token -map results/mapping.txt -offset tmp/offset.txt
echo parsing ...
./bin/segphrase_parser results/segmentation.model results/salient.csv 5000 tmp/test.token tmp/test.parsed.txt 0
echo decoding ...
${PYPY} src/online_query/decoding.py -i tmp/test.parsed.txt -o tmp/test.result -map results/mapping.txt -orig ${RAW_TEXT} -offset tmp/offset.txt

${PYPY} src/online_query/compute_offset.py tmp/test.result results/offset.txt
