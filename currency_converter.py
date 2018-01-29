#!/usr/bin/env python3

from converter.converter import *
import argparse

# parsing input parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    "--amount", help="amount which we want to convert", required=True, type=float)
parser.add_argument("--input_currency",
                    help="input currency - 3 letters name or currency symbol", required=True, type=str)
parser.add_argument("--output_currency",
                    help="output currency - 3 letters name or currency symbol", type=str, default="")

args = parser.parse_args()

try:
    # try to make output dictionary
    result = make_output(
        args.amount, args.input_currency, args.output_currency)

    # print result
    print(to_json(result))

# unknow currency code / connection to ECB couldn't be established
except Exception as err:
    print(err)
