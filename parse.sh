TOP_K=5
OFFSET=1

./bin/segphrase_parser results/segmentation.model results/salient.csv 50000 $1 $2 0 ${TOP_K} ${OFFSET}
# python ./src/online_query/compute_offset.py ./results/parsed.txt ./results/offset.txt
