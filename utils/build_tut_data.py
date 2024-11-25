import enum
import os
import argparse
import random
from nltk import Tree
from stanza.models.constituency import tree_reader, parse_tree
from supar.models.const.crf.transform import Tree as SuparTree


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Build train, test, valid datset from tut Italian treebank."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Path to the directory containing .penn treebank files.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Path to store cleaned treebank files and flat trees."
        "If not provided, saves in the same directory as input_dir.",
    )
    parser.add_argument(
        "--train_ratio",
        type=float,
        default=0.7,
        help="Proportion of the combined data to use for training.",
    )
    parser.add_argument(
        "--test_ratio",
        type=float,
        default=0.15,
        help="Proportion of the combined data to use for testing.",
    )
    parser.add_argument(
        "--val_ratio",
        type=float,
        default=0.15,
        help="Proportion of the combined data to use for validation.",
    )
    return parser.parse_args()


def clean_file(in_file, out_file):
    with open(in_file, "r", encoding="utf-8") as f:
        text = f.readlines()
    with open(out_file, "w", encoding="utf-8") as f:
        for t in text:
            if not t.startswith("*"):
                f.writelines(t)
    print(f"Cleaned trees saved at: {out_file}")


def flatten_trees(in_file, out_file):
    flat_trees = tree_reader.read_tree_file(in_file)
    flat_trees = [t.children[0] for t in flat_trees]
    parse_tree.Tree.write_treebank(flat_trees, out_file)
    print(f"Flat trees at: {out_file}")


def get_malformed_idx(trees):
    bad_trees = []
    for i, t in enumerate(trees):
        try:
            t = Tree.fromstring(t)
            SuparTree.binarize(t)
        except AttributeError as e:
            print(e)
            bad_trees.append(i)
    return bad_trees


def split_train_test_valid(data, train_ratio, test_ratio, val_ratio):
    random.seed(42)
    random.shuffle(data)

    print(sum([train_ratio, test_ratio, val_ratio]))

    total = len(data)
    train_end = int(total * train_ratio)
    test_end = train_end + int(total * test_ratio)

    train = data[:train_end]
    test = data[train_end:test_end]
    val = data[test_end:]

    return train, test, val


def main():
    args = parse_arguments()

    # Set default output file path if not provided
    if args.output_dir is None:
        args.output_dir = args.input_dir

    for fname in os.listdir(args.input_dir):
        if fname.endswith(".penn"):
            corpus_name, _ = os.path.splitext(fname)
            temp_path = os.path.join(args.output_dir, corpus_name + ".clean")
            clean_file(os.path.join(args.input_dir, fname), temp_path)
            flatten_trees(
                temp_path, os.path.join(args.output_dir, corpus_name + ".flat")
            )

    combined_files = []
    for fname in os.listdir(args.output_dir):
        if fname.endswith(".flat"):
            with open(os.path.join(args.output_dir, fname), "r", encoding="utf-8") as f:
                combined_files.extend(f.readlines())

    bad_idx = get_malformed_idx(combined_files)
    print(f"Found {len(bad_idx)} malformed trees at {bad_idx}, removing them.")
    combined_files = [t for i, t in enumerate(combined_files) if i not in bad_idx]
    print(f"Remaining items: {len(combined_files)}")

    train, test, val = split_train_test_valid(
        combined_files, args.train_ratio, args.test_ratio, args.val_ratio
    )

    for data, ext in zip([train, test, val], ["train", "test", "val"]):
        fname = os.path.join(args.output_dir, f"combined.{ext}")
        with open(fname, "w", encoding="utf-8") as f:
            f.writelines(data)
        print(f"Combined {ext} dataset saved at: {fname}")


if __name__ == "__main__":
    main()
