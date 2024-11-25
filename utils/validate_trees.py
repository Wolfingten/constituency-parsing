from nltk import Tree
from supar.models.const.crf.transform import Tree as SuparTree


def test_child_label_in_file(file_path):
    """
    Tests every tree in a file to ensure all child nodes are valid for the operation:
    `child[:] = [nltk.Tree(child.label(), child[:])]`.

    Args:
        file_path (str): Path to the input file containing constituency trees in bracket notation.

    Returns:
        None. Prints results to the console.
    """
    malformed_trees = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Testing {len(lines)} trees in {file_path}...")
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        try:
            # Parse the tree
            tree = Tree.fromstring(line)

            # Attempt to binarize the tree
            SuparTree.binarize(tree)

        except AttributeError as e:
            # Capture AttributeError specifically related to `label` or invalid children
            if "label" in str(e):
                malformed_trees.append((i, line, str(e)))

    # Report results
    if malformed_trees:
        print(f"\nFound {len(malformed_trees)} trees with invalid child nodes:")
        for line_number, tree_string, error in malformed_trees:
            print(f"Line {line_number}: {tree_string}\n  Error: {error}")
    else:
        print("All trees passed the validation.")


file_path = "/home/wolfingten/projects/data/tut/combined.train"  # Replace with the path to your file
test_child_label_in_file(file_path)
