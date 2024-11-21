from supar import Parser

# load multilingual parser
parser = Parser.load("con-crf-xlmr")

with open("/data/users/jguertler/datasets/tut/NEWS.seg", "r") as f:
    text = f.readlines()

dataset = parser.predict(
    text,
    pred="/data/users/jguertler/datasets/tut/NEWS.pred",
    lang="it",
)
