#!/bin/sh

python /self-attentive-parser/src/main.py train \
  --train-path /data/users/jguertler/data/tut/combined.train \
  --dev-path /data/users/jguertler/data/tut/combined.test \
  --evalb-dir /self-attentive-parser/EVALB \
  --use-pretrained --pretrained-model "bert-base-multilingual-cased" \
  --use-encoder --num-layers 2 \
  --predict-tags \
  --model-path-base /data/users/jguertler/models/it_bert_base_multilingual_cased
