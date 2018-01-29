#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import json

__name__ = 'converter'

# supported currencies symbols
currency_symbols = {
    '$': 'USD',
    'jp¥': 'JPY',
    'kč': 'CZK',
    'dkr': 'DKK',
    '£': 'GBP',
    'ft': 'HUF',
    'zł': 'PLN',
    'skr': 'SEK',
    'nkr': 'NOK',
    'kn': 'HRK',
    'tl': 'TRY',
    'au$': 'AUD',
    'r$': 'BRL',
    'ca$': 'CAD',
    '¥': 'CNY',
    'hk$': 'HKD',
    'rp': 'IDR',
    '₪': 'ILS',
    'rs': 'INR',
    '₩': 'KRW',
    'mx$': 'MXN',
    'rm': 'MYR',
    'nz$': 'NZD',
    '₱': 'PHP',
    's$': 'SGD',
    '฿': 'THB',
    'r': 'ZAR',
    '€': 'EUR'
}


def retrieve_exchange_rates():
    """
    Function retrieving actual exchange rates for major world currencies.
    All rates are against the euro (base currency)

    Source: European central bank (xml format), updated every working day around 16:00
    Returns: Dictionary of exchange rates in format 'currency_code' : exchange rate ,
    e.g. {'USD' : 1.22 , 'CZK' : 25.3 , ...}
    """

    # data source
    ecb_xml = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(ecb_xml)

    if response.status_code != 200:
        raise ValueError(
            "Not able to retrieve current exchange rates table from ECB. Response status code: {}".format(response.status_code))

    # XML tree
    root = ET.fromstring(response.text)
    currencies = root[2][0]

    # creation of dictionary
    exchange_rates = {child.attrib['currency']: float(
        child.attrib['rate']) for child in currencies}

    # add EUR
    exchange_rates['EUR'] = 1.0

    return exchange_rates


def exchange(from_currency, to_currency, amount):
    """
    Function converting money from one currency to another
    Args:     from_currency: Input currency
              to_currency: Output currency
              amount: Amount of money to transfer
    Returns: Converted amount
    """

    try:
        exchange_rates = retrieve_exchange_rates()
    except e:
        raise e

    # all math is here
    return (amount / exchange_rates[from_currency]) * exchange_rates[to_currency]


def currency_code(currency):
    """
    Function checks if currency symbol/code is known and returns uppercase currency code
    Args: Currency symbol or code
    Returns: Currency uppercase code
    """

    # is currency symbol known?
    if currency.lower() in currency_symbols.keys():
        return currency_symbols[currency.lower()]
    # is  currency code known?
    elif currency.upper() in currency_symbols.values():
        return currency.upper()
    # currency not found
    else:
        err_msg = "Unknown currency symbol/code : {}".format(currency)
        raise ValueError(err_msg)


def make_output(amount, input_code, output_cur):
    """
    Function preparing results of app
    Args: amount - amount of money we want to convert
          input_code - input currency code, so we can exclude it from results
          output_cur - empty string ("") for conversion to all known currencies or currency symbol/code
    Returns: dictionary containing currency codes and converted values {"currency_code": value}
    """

    try:
        # convert to specific currency
        if(output_cur != ""):
            # try to translate currency code/symbol
            output_currency = currency_code(output_cur)
            output_dict = {
                output_currency: exchange(input_code, output_currency, amount)
            }
        # convert to all known currencies
        else:
            output_dict = {
                currency: exchange(input_code, currency, amount)
                for currency in currency_symbols.values()
            }
            output_dict.pop(input_code)

    # currency symbol/code is unknown
    except Exception as err:
        raise err

    return output_dict


def to_json(input_dict, output_dict):
    """
    Function returning final output of app by combining input and output dictionaries.
    Args: input dictionary in form {"amount": value, "currency" : code}
          output dictionary in form {"currency_code": converted value, ...}
    Returns: JSON from dictionary in form : {"input": input_dict, "output": output_dict}
    """

    result = {
        "input": input_dict,
        "output": output_dict
    }

    return json.dumps(result, sort_keys=True, indent=4, separators=(",", ": "))
