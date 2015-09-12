#!/bin/bash

export PYTHON=python
export PYPY=pypy

RAW_TEXT=data/wiki.cleaned.txt
PHRASE_LIST=results/salient.csv.natural

AUTO_LABEL=1
DATA_LABEL=data/wiki.label.auto
KNOWLEDGE_BASE=data/wiki_labels_quality.txt
KNOWLEDGE_BASE_LARGE=data/wiki_labels_all.txt

STOPWORD_LIST=data/stopwords.txt
SUPPORT_THRESHOLD=10

OMP_NUM_THREADS=10
DISCARD_RATIO=0.05
MAX_ITERATION=5
TOP_K=5
ALPHA=0.85

SLIDING_WINDOW=10
SLIDING_THRES=0.5

# clearance
# rm -rf tmp
# rm -rf results

mkdir -p tmp
mkdir -p results

Green='\033[0;32m'
NC='\033[0m'

# # preprocessing
# echo -e "${Green}Translating traditional Chinese to simplified using OpenCC${NC}" 
# opencc -i ${RAW_TEXT} -o tmp/pre_raw.txt -c tw2s.json

# echo -e "${Green}Transforming punctuations${NC}"
# ${PYPY} ./src/preprocessing/punctuation.py -i tmp/pre_raw.txt -o tmp/raw.txt

# echo -e "${Green}Doing Chinese word segmentation and tokenization${NC}"
# ${PYPY} ./src/preprocessing/tokenization.py -i tmp/raw.txt -o tmp/raw.txt.token -map results/mapping.txt

# echo -e "${Green}Transforming to binary format${NC}"
# ./bin/from_raw_to_binary_text tmp/raw.txt.token tmp/sentencesWithPunc.buf

# #frequent phrase mining for phrase candidates
# echo -e "${Green}Mining frequent phrases as candidates${NC}"
# ${PYTHON} ./src/frequent_phrase_mining/main.py -thres ${SUPPORT_THRESHOLD} -o ./results/patterns.csv -raw tmp/raw.txt.token
# ${PYTHON} ./src/preprocessing/compute_idf.py -raw tmp/raw.txt.token -o results/wordIDF.txt

# #feature extraction
# echo -e "${Green}Extracting features${NC}"
# ${PYPY} ./src/utils/encoding.py results/mapping.txt ${STOPWORD_LIST}
# ./bin/feature_extraction tmp/sentencesWithPunc.buf results/patterns.csv ${STOPWORD_LIST}.token results/wordIDF.txt results/feature_table_0.csv

# if [ ${AUTO_LABEL} -eq 1 ];
# then
# 	echo -e "${Green}Auto labeling${NC}"
# 	${PYPY} ./src/utils/encoding.py results/mapping.txt ${KNOWLEDGE_BASE} ${KNOWLEDGE_BASE_LARGE}
#     ${PYTHON} src/classification/auto_label_generation.py ${KNOWLEDGE_BASE}.token ${KNOWLEDGE_BASE_LARGE}.token results/feature_table_0.csv results/patterns.csv ${DATA_LABEL}
# fi

# # classifier training
# echo -e "${Green}Classifying using random forests${NC}"
# ./bin/predict_quality results/feature_table_0.csv ${DATA_LABEL} results/ranking.csv outsideSentence,log_occur_feature,constant,frequency 0 TRAIN results/random_forest_0.model

# MAX_ITERATION_1=$(expr $MAX_ITERATION + 1)

# # 1-st round
# echo -e "${Green}First round phrasal segmentation${NC}"
# ./bin/from_raw_to_binary tmp/raw.txt.token tmp/sentences.buf
# ./bin/adjust_probability tmp/sentences.buf ${OMP_NUM_THREADS} results/ranking.csv results/patterns.csv ${DISCARD_RATIO} ${MAX_ITERATION} ./results/ ${DATA_LABEL} ./results/penalty.1 ${TOP_K}

# # 2-nd round
# echo -e "${Green}Recomputing features${NC}"
# ./bin/recompute_features results/iter${MAX_ITERATION_1}_discard${DISCARD_RATIO}/length results/feature_table_0.csv results/patterns.csv tmp/sentencesWithPunc.buf results/feature_table_1.csv ./results/penalty.1 1

# echo -e "${Green}Second round phrasal segmentation${NC}"
# ./bin/predict_quality results/feature_table_1.csv ${DATA_LABEL} results/ranking_1.csv outsideSentence,log_occur_feature,constant,frequency 0 TRAIN results/random_forest_1.model
# ./bin/adjust_probability tmp/sentences.buf ${OMP_NUM_THREADS} results/ranking_1.csv results/patterns.csv ${DISCARD_RATIO} ${MAX_ITERATION} ./results/1. ${DATA_LABEL} ./results/penalty.2 ${TOP_K}

# # phrase list & segmentation model
# echo -e "${Green}Preparing phrase lists and segmentation model${NC}"
# ./bin/prune_and_combine results/1.iter${MAX_ITERATION_1}_discard${DISCARD_RATIO}/length ${SLIDING_WINDOW} ${SLIDING_THRES} results/phrase_list.txt DET results/phrase_list.stat
# ./bin/build_model results/1.iter${MAX_ITERATION_1}_discard${DISCARD_RATIO}/ 6 ./results/penalty.2 results/segmentation.model

# echo -e "${Green}Word2vec embedding${NC}"
# # unigrams
# normalize_text() {
#   awk '{print tolower($0);}' | sed -e "s/’/'/g" -e "s/′/'/g" -e "s/''/ /g" -e "s/'/ ' /g" -e "s/“/\"/g" -e "s/”/\"/g" \
#   -e 's/"/ " /g' -e 's/\./ \. /g' -e 's/<br \/>/ /g' -e 's/, / , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' \
#   -e 's/\?/ \? /g' -e 's/\;/ /g' -e 's/\:/ /g' -e 's/-/ - /g' -e 's/=/ /g' -e 's/=/ /g' -e 's/*/ /g' -e 's/|/ /g' \
#   -e 's/«/ /g' | tr 0-9 " "
# }
# normalize_text < results/1.iter${MAX_ITERATION}_discard${DISCARD_RATIO}/segmented.txt > tmp/normalized.txt

# echo -e "${Green}Propagating quality score to unigrams${NC}"
# cd word2vec_tool
# make
# cd ..
# ./word2vec_tool/word2vec -train tmp/normalized.txt -output ./results/vectors.bin -cbow 2 -size 300 -window 6 -negative 25 -hs 0 -sample 1e-4 -threads ${OMP_NUM_THREADS} -binary 1 -iter 15
# time ./bin/generateNN results/vectors.bin results/1.iter${MAX_ITERATION_1}_discard${DISCARD_RATIO}/ 30 3 results/u2p_nn.txt results/w2w_nn.txt
# ./bin/qualify_unigrams results/vectors.bin results/1.iter${MAX_ITERATION_1}_discard${DISCARD_RATIO}/ results/u2p_nn.txt results/w2w_nn.txt ${ALPHA} results/unified.csv 100 ${STOPWORD_LIST}.token

# echo -e "${Green}Generating final results${NC}"
# ${PYTHON} src/postprocessing/filter_by_support.py results/unified.csv results/1.iter5_discard0.05/segmented.txt ${SUPPORT_THRESHOLD} results/salient.csv 
${PYPY} src/utils/decoding.py results/mapping.txt results/salient.csv ${PHRASE_LIST}
