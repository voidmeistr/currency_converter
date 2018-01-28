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

input_dict = {}
output_dict = {}

try:
    # try to translate currency code/symbol
    input_currency = currency_code(args.input_currency)
    input_dict['amount'] = args.amount
    input_dict['currency'] = input_currency

    # output currency is defined
    if(args.output_currency != ""):
        output_currency = currency_code(args.output_currency)
        output_dict[output_currency] = exchange(
            input_currency, output_currency, args.amount)
    # convert to all known currencies
    else:
        output_dict = {currency: exchange(
            input_currency, currency, args.amount) for currency in currency_symbols.values()}
        # except input currency
        output_dict.pop(input_currency)

    # create result dictionary
    result = {}
    result["input"] = input_dict
    result["output"] = output_dict

    print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))

except Exception as err:
    print(err)
