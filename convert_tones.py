import argparse
import pandas as pd
import os

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("the file %s does not exist" % arg)
    elif arg.endswith('.tsv'):
        return pd.read_csv(arg, sep="\t", encoding="utf-8")
    elif arg.endswith('.csv'):
        return pd.read_csv(arg, encoding="utf-8")
    else:
        parser.error("the file must be a tsv or csv file")

parser = argparse.argumentparser(description="convert to and from tone classes and single character tone values")
parser.add_argument("-i", dest="input_df", required=True, help="A tsv or csv file with dialect data as columns", metavar="INPUT")
