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
    # try to translate currency code/symbol
    input_currency = currency_code(args.input_currency)
    input_dict = {
        "amount": args.amount,
        "currency": currency_code(input_currency)
    }

    # try to make output dictionary
    output_dict = make_output(
        args.amount, input_currency, args.output_currency)

    # print result
    print(to_json(input_dict, output_dict))

# unknow currency code / connection to ECB couldn't be established
except Exception as err:
    print(err)
