import os
import re
import csv
import argparse
import stanza

LANG_CODES = {
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Italian": "it",
    "Korean": "ko",
    "Norwegian": "no",
    "Russian": "ur",
    "Spanish": "es",
    "Turkish": "tr",
}


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Split meco stories csv data into separate files by language."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Path to the output dir. "
        "If not provided, saves in the same directory as input_file.",
    )
    return parser.parse_args()


def segment_setnences(row, lang):
    nlp = stanza.Pipeline(lang=lang, processors="tokenize")
    doc = nlp(" ".join(row))
    sentences = []
    for s in doc.sentences:
        sent = " ".join([token.text for token in s.tokens])
        sent = re.sub(r"\\n", "", sent)
        sentences.append(sent)
    return sentences


def main():
    args = parse_arguments()

    if args.output_dir is None:
        input_dir = os.path.dirname(args.input_file)
        args.output_dir = input_dir

    with open(args.input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        for row in reader:
            if row[0]:
                lang = row[0]
                print(f"Processing {lang}")
                filename = f"{lang}.txt"  # Assumes the first column contains unique identifiers
                output_file = os.path.join(args.output_dir, filename)

                sentences = segment_setnences(row[1:], LANG_CODES[lang])

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(sentences))

                print(f"written to {output_file}")


if __name__ == "__main__":
    main()
