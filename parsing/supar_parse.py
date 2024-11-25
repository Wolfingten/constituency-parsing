# from supar import Parser
#
## load multilingual parser
# parser = Parser.load("con-crf-xlmr")
#
# with open("/data/users/jguertler/datasets/tut/NEWS.seg", "r") as f:
#    text = f.readlines()
#
# dataset = parser.predict(
#    text,
#    pred="/data/users/jguertler/datasets/tut/NEWS.pred",
#    lang="it",
# )

import argparse
import os
from supar import Parser


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
        "--output_file",
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

    # Set default output file path if not provided
    if args.output_file is None:
        input_dir = os.path.dirname(args.input_file)
        input_filename = os.path.basename(args.input_file)
        base_name, _ = os.path.splitext(input_filename)
        args.output_file = os.path.join(input_dir, f"{base_name}.supar")

    if args.lang == "en":
        parser = Parser.load("con-crf-roberta-en")
    else:
        # Load multilingual parser
        parser = Parser.load("con-crf-xlmr")

    with open(args.input_file, "r", encoding="utf-8") as f:
        text = f.readlines()

    parser.predict(
        text,
        pred=args.output_file,
        lang=args.lang,
    )

    print(f"Parses saved to {args.output_file}")


if __name__ == "__main__":
    main()
