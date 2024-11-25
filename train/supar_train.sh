#!/bin/sh

python -u -m supar.cmds.const.crf train -b -d 0 -c con-crf-roberta-en -p model  \
    --train /home/wolfingten/projects/data/tut/combined.train  \
    --dev /home/wolfingten/projects/data/tut/combined.val  \
    --test /home/wolfingten/projects/data/tut/combined.test  \
    --encoder=bert  \
    --bert=xlm-roberta-large  \
    --lr=5e-5  \
    --lr-rate=20  \
    --epochs=10  \
    --update-steps=4

#    --batch-size=5000  \
