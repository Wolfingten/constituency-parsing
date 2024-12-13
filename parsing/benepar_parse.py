import os
import argparse
import spacy
import benepar


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run supar a multilingual parser on input text and save predictions."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input file containing text to parse.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Path to the output file where predictions will be saved. "
        "If not provided, saves in the same directory as input_file with '.supar' extension.",
    )
    parser.add_argument(
        "--lang",
        type=str,
        help="Language code for parsing.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.input_file)

    with open(args.input_file, "r", encoding="utf-8") as f:
        stories = f.readlines()

    nlp = spacy.load("xx_sent_ud_sm")
    nlp.add_pipe("benepar", config={"model": "/data/users/jguertler/models/it_bert_base_multilingual_cased_dev=5118.92.pt"})

    parses = []
    for s in stories:
        doc = nlp(" ".join(s.split()))
        sent = list(doc.sents)[0]
        parses.append(sent._.parse_string)

    with open(os.path.join(args.output_dir, "parse.benepar"), "w", encoding="utf-8") as f:
        for p in parses:
            f.write(f"{p}\n")

if __name__ == "__main__":
    main()
